import base64
import zlib
from urllib.parse import quote, urlencode, parse_qs, unquote_plus
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
            parameters['RelayState'] = quote(relay_state)

        # Append the parameters on the uri and return.
        uri = '%s?%s' % (uri, urlencode(parameters))
        return uri, None

    raise ValueError('unknown protocol', protocol)


def receive(method, query_string, body):

    # Parse the query string.
    query = parse_qs(query_string)

    # Determine the protocol used.
    method = method.upper()
    if method == 'GET':
        protocol = 'artifact' if 'SAMLArtifact' in query else 'redirect'

    elif method == 'POST':
        protocol = 'post'

    else:
        # Unknown method used.
        return None

    if protocol == 'redirect':
        # Pull the text out of the query.
        encoded = query.get('SAMLResponse', query.get('SAMLRequest'))
        if not encoded:
            # No SAML message found.
            return None

        # Decode the text.
        text = zlib.decompress(base64.b64decode(encoded[0]), -15)

        # Parse the text into xml.
        message = etree.XML(text)

        # Get the relay state if present.
        relay_state = query.get('RelayState')
        if relay_state:
            relay_state = unquote_plus(relay_state[0])

        # Return the message and the relay state.
        return message, relay_state
