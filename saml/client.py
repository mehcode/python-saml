# -*- coding: utf-8 -*-
import base64
import zlib
import six
from six.moves.urllib.parse import quote, urlencode, parse_qs, unquote_plus
from lxml import etree
from saml import schema
from saml.schema.base import _element_registry


def send(uri, message, relay_state=None, protocol='redirect'):

    # Determine the name of parameter.
    element = _element_registry.get(message.tag)
    if not element:
        raise ValueError('unknown element', message)

    if protocol == 'redirect':
        # For sending a message through redirection; we need
        # to encode the message (depending on what it is) in the URI
        # as SAMLRequest or SAMLResponse.
        name = 'SAMLRequest'
        if isinstance(element, schema.StatusResponse):
            name = 'SAMLResponse'

        # Serialize and encode the message.
        text = base64.b64encode(zlib.compress(etree.tostring(message))[2:-4])

        # Build the parameters.
        parameters = {name: text}
        if relay_state:
            parameters['RelayState'] = relay_state

        # Append the parameters on the uri and return.
        uri = '%s?%s' % (uri, urlencode(parameters))
        return uri, None

    raise ValueError('unknown protocol', protocol)


def _text(str_or_bytes):
    if isinstance(str_or_bytes, six.text_type):
        return str_or_bytes

    return str_or_bytes.decode()


def receive(method, query_string, body):
    # Determine the protocol used and pare the appropriate data.
    method = method.upper()
    if method == 'GET':
        data = parse_qs(_text(query_string))
        binding = 'artifact' if 'SAMLArtifact' in data else 'redirect'

    elif method == 'POST':
        data = parse_qs(_text(body))
        binding = 'post'

    else:
        # Unknown method used.
        return None

    if binding in ('redirect', 'post'):
        # Pull the text out of the query.
        encoded = data.get('SAMLResponse', data.get('SAMLRequest'))
        if not encoded:
            # No SAML message found.
            return None

        # Decode the text.
        text = base64.b64decode(encoded[0])
        if binding == "redirect":
            text = zlib.decompress(text, -15)

        # Parse the text into xml.
        message = etree.XML(text)

        # Get the relay state if present.
        relay_state = data.get('RelayState')
        if relay_state:
            relay_state = unquote_plus(relay_state[0])

        # Return the message and the relay state.
        return message, relay_state
