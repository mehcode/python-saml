"""Security Assertion Markup Language (SAML) v2.0

A python interface to produce and consume Security Assertion Markup
Language (SAML) v2.0 messages.

@par References
    - https://www.oasis-open.org/standards#samlv2.0
"""

#! Version of the library.
from .meta import version as __version__
VERSION = __version__

#! Version of the SAML standard supported.
from .schema import VERSION as SAML_VERSION

from .signature import sign, verify

__all__ = [
    'VERSION',
    'SAML_VERSION',
    'sign',
    'verify'
]
