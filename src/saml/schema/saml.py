""" \file saml/schema/saml.py
\brief Defines the XML data types for SAML2 in the saml namespace.

\author Ryan Leckey (mehcode) leckey.ryan@gmail.com

\copyright Copyright © 2012 Concordus Applications, Inc.
           \n \n
           Permission is hereby granted, free of charge, to any person
           obtaining a copy of this software and associated documentation
           files (the "Software"), to deal in the Software without restriction,
           including without limitation the rights to use, copy, modify, merge,
           publish, distribute, sublicense, and/or sell copies of the Software,
           and to permit persons to whom the Software is furnished to do so,
           subject to the following conditions:
           \n \n
           The above copyright notice and this permission notice shall be
           included in all copies or substantial portions of the Software.
           \n \n
           THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
           EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
           MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
           NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
           BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
           ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
           CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
           SOFTWARE.
"""
import abc
from .. import schema
from uuid import uuid4
from datetime import datetime


class Element(schema.Element):
    """Represents an element in this namespace."""
    namespace = ("saml", "urn:oasis:names:tc:SAML:2.0:assertion")


class BaseIDAbstractType(schema.Type):
    """
    Provides an extension point that allows applications to add new kinds of
    identifiers.
    """

    __metaclass__ = abc.ABCMeta

    ## The security or administrative domain that qualifies the name.
    name_qualifier = schema.Attribute("NameQualifier")

    ## Further qualifies a name with the name of a service provider or
    ## affiliation of providers.
    sp_name_qualifier = schema.Attribute("SPNameQualifier")


class NameIDType(BaseIDAbstractType):
    """
    Used when an element serves to represent an entity by a string-valued name.
    It is a more restricted form of identifier than the <BaseID> element and
    is the type underlying both the <NameID> and <Issuer> elements.

    In addition to the string content containing the actual identifier, it
    provides the following optional attributes.
    """

    class Format:
        ## The interpretation of the attribute name is left to individual
        ## implementations.
        UNSPECIFIED = "urn:oasis:names:tc:SAML:1.0:nameid-format:unspecified"

        ## Indicates that the content of the element is in the form of an email
        ## address.
        EMAIL = "urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress"

        ## Indicates that the content of the element is in the form specified
        ## for the contents of the <ds:X509SubjectName> element in the XML
        ## Signature Recommendation [XMLSig].
        X509 = "urn:oasis:names:tc:SAML:1.1:nameid-format:X509SubjectName"

        ## Indicates that the content of the element is a Windows domain
        ## qualified name.
        WINDOWS = (
            "urn:oasis:names:tc:SAML:1.1:nameid-format"
            ":WindowsDomainQualifiedName")

        ## Indicates that the content of the element is in the form of a
        ## Kerberos principal name using the format name[/instance]@REALM.
        KEREBOS = "urn:oasis:names:tc:SAML:2.0:nameid-format:kerberos"

        ## Indicates that the content of the element is the identifier of an
        ## entity that provides SAML-based services.
        ENTITY = "urn:oasis:names:tc:SAML:2.0:nameid-format:entity"

        ## Indicates that the content of the element is a persistent opaque
        ## identifier for a principal that is specific to an identity provider
        ## and a service provider or affiliation of service providers.
        PERSISTENT = "urn:oasis:names:tc:SAML:2.0:nameid-format:persistent"

        ## Indicates that the content of the element is an identifier with
        ## transient semantics and SHOULD be treated as an opaque and
        ## temporary value by the relying party.
        TRANSIENT = "urn:oasis:names:tc:SAML:2.0:nameid-format:transient"

    ## A URI reference representing the classification of string-based
    ## identifier information.
    format = schema.Attribute("Format", default=Format.UNSPECIFIED)

    ## A name identifier established by a service provider or affiliation of
    ## providers for the entity, if different from the primary name
    ## identifier given in the content of the element.
    sp_provided_id = schema.Attribute("SPProvidedID")


class NameID(Element, NameIDType):
    """
    Is of type NameIDType (see Section 2.2.2), and is used in various SAML
    assertion constructs such as the <Subject> and <SubjectConfirmation>
    elements, and in various protocol messages.
    """


## \todo Element : <EncryptedID>
## \todo Type    : EncryptedElementType


class Issuer(Element, NameIDType):
    """
    Provides information about the issuer of a SAML assertion or protocol
    message.
    """

    ## Overriding the usual rule for this element's type, if no Format value is
    ## provided with this element, then the value \ref ENTITY is in effect.
    format = schema.Attribute("Format", default=NameID.Format.ENTITY)


## \todo Element    : <AssertionIDRef>
## \todo Element    : <AssertionURIRef>


class AssertionType(schema.Type):
    """Specifies the basic information that is common to all assertions."""


class Assertion(Element, AssertionType):
    """Specifies the basic information that is common to all assertions."""

    ## The version of this assertion. The identifier for the version of SAML
    ## defined in this specification is "2.0".
    version = schema.Attribute(
        "Version",
        required=True,
        default="2.0")

    ## The identifier for this assertion.
    id = schema.Attribute(
        "ID",
        required=True,
        default=lambda: '_{}'.format(uuid4().hex))

    ## The time instant of issue in UTC.
    issue_instant = schema.Attribute(
        "IssueInstant",
        required=True,
        default=lambda: datetime.utcnow())

    ## The SAML authority that is making the claim(s) in the assertion.
    issuer = Issuer(required=True)
