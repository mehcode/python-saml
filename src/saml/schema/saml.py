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
from .. import VERSION
from .. import schema
from uuid import uuid4
from datetime import datetime


class Type(schema.Type):
    """Represents a type in this namespace."""
    namespace = ("saml", "urn:oasis:names:tc:SAML:2.0:assertion")


class BaseIDAbstractType(Type):
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


class NameID(NameIDType):
    """
    Is of type NameIDType (see Section 2.2.2), and is used in various SAML
    assertion constructs such as the <Subject> and <SubjectConfirmation>
    elements, and in various protocol messages.
    """


## \todo Element : <EncryptedID>
## \todo Type    : EncryptedElementType


class Issuer(NameIDType):
    """
    Provides information about the issuer of a SAML assertion or protocol
    message.
    """

    ## Overriding the usual rule for this element's type, if no Format value is
    ## provided with this element, then the value \ref ENTITY is in effect.
    format = schema.Attribute("Format", default=NameID.Format.ENTITY)


## \todo Element    : <AssertionIDRef>
## \todo Element    : <AssertionURIRef>


class SubjectConfirmationData(Type):
    """
    Specifies additional data that allows the subject to be confirmed or
    constrains the circumstances under which the act of subject confirmation
    can take place.
    """

    ## \todo Support for KeyInfoConfirmationDataType

    ## \todo Support for arbitrary attributes
    ## \todo Support for arbitrary elements

    ## A time instant before which the subject cannot be confirmed.
    not_before = schema.DateTimeAttribute("NotBefore")

    ## A time instant at which the subject can no longer be confirmed.
    not_on_or_after = schema.DateTimeAttribute("NotOnOrAfter")

    ## A URI specifying the entity or location to which an attesting entity
    ## can present the assertion.
    recipient = schema.Attribute("Recipient")

    ## The ID of a SAML protocol message in response to which an attesting
    ## entity can present the assertion.
    in_response_to = schema.Attribute("InResponseTo")

    ## The network address/location from which an attesting entity can
    ## present the assertion.
    address = schema.Attribute("Address")


class SubjectConfirmation(Type):
    """
    Provides the means for a relying party to verify the correspondence of the
    subject of the assertion with the party with whom the relying party is
    communicating.
    """

    ## \todo class Method: Enumeration of values available

    ## A URI reference that identifies a protocol or mechanism to be used to
    ## confirm the subject.
    method = schema.Attribute("Method", required=True)

    ## Identifies the entity expected to satisfy the enclosing subject
    ## confirmation requirements.
    id = schema.Element(BaseIDAbstractType)

    ## Additional confirmation information to be used by a specific
    ## confirmation method.
    data = schema.Element(SubjectConfirmationData)


class Subject(Type):
    """
    Specifies the principal that is the subject of all of the (zero or more)
    statements in the assertion.
    """
    ## Identifies the subject.
    id = schema.Element(BaseIDAbstractType)

    ## Information that allows the subject to be confirmed.
    confirm = schema.Element(SubjectConfirmation)


class Assertion(Type):
    """Specifies the basic information that is common to all assertions."""

    ## The version of this assertion. The identifier for the version of SAML
    ## defined in this specification is "2.0".
    version = schema.Attribute("Version", required=True, default=VERSION)

    ## The identifier for this assertion.
    id = schema.Attribute(
        "ID",
        required=True,
        default=lambda: '_{}'.format(uuid4().hex))

    ## The time instant of issue in UTC.
    issue_instant = schema.DateTimeAttribute(
        "IssueInstant",
        required=True,
        default=datetime.utcnow)

    ## The SAML authority that is making the claim(s) in the assertion.
    issuer = schema.Element(Issuer, min_occurs=1)

    ## \todo Element <ds:Signature>

    ## The subject of the statement(s) in the assertion.
    subject = schema.Element(Subject)

    ## Conditions that MUST be evaluated when assessing the validity of and/or
    ## when using the assertion.
    ## \todo conditions = schema.Element(Conditions)

    ## Additional information related to the assertion that assists
    ## processing in certain situations but which MAY be ignored by
    ## applications that do not understand the advice or do not wish to make
    ## use of it.
    ## \todo advice = schema.Element(Advice)

    ## The collection of statements asserted by this assertion.
    #statements = schema.Element(Statement, max_occurs=None)


## \todo Element <EncryptedAssertion>
## \todo Element <Condition>
## \todo Elements <AudienceRestriction> and <Audience>
## \todo Element <OneTimeUse>
## \todo Element <ProxyRestriction>
## \todo Element <Advice>
## \todo Element <Statement>
## \todo Element <AuthnStatement>
## \todo Element <SubjectLocality>
## \todo Element <AuthnContext>
## \todo Element <AttributeStatement>
## \todo Element <Attribute>
## \todo Element <AttributeValue>
## \todo Element <EncryptedAttribute>
## \todo Element <AuthzDecisionStatement>
## \todo Simple Type DecisionType
## \todo Element <Action>
## \todo Element <Evidence>
