# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
from saml.schema import samlp


def authenticate(name):
    """Generates a SAML Authentication Request."""
    # Construct the request
    message = samlp.AuthnRequest(
        issuer=saml.Issuer(value='saml://{}'.format(name)),
    ).tostring()


def assertion_consumer_service():
    """Handles the 'Assertion Consumer Service'."""
    pass
