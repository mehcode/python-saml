"""Security Assertion Markup Language (SAML) v2.0

A python interface to produce and consume Security Assertion Markup
Language (SAML) v2.0 messages.

@par References
    - https://www.oasis-open.org/standards#samlv2.0
"""
#! Version of the library.
from ._version import __version__, __version_info__  # noqa
VERSION = __version__

#! Version of the SAML standard supported.
from .schema import VERSION as SAML_VERSION

from .signature import sign, verify
from . import client

__all__ = [
    'VERSION',
    'SAML_VERSION',
    'sign',
    'verify',
    'client'
]
