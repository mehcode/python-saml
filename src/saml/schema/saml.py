# -*- coding: utf-8 -*-
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
from uuid import uuid4
from datetime import datetime
from .. import VERSION
from . import attribute, element


class Element(element.Element):
    class Meta(element.Element.Meta):
        namespace = ("saml", "urn:oasis:names:tc:SAML:2.0:assertion")


class BaseIDAbstractType(Element):
    """Provides an extension point for identifiers.
    """

    ## The security or administrative domain that qualifies the name.
    name_qualifier = attribute.Attribute("NameQualifier")

    ## Further qualifies a name with the name of a service provider.
    sp_name_qualifier = attribute.Attribute("SPNameQualifier")


class NameIDType(BaseIDAbstractType):
    """Serves to represent an entity by a string-valued name.
    """

    class Format:
        """Enumerates accepted values for \ref NameID.format.
        """

        ## URI prefix for the values in this enumeration.
        _PREFIX = "urn:oasis:names:tc:SAML:1.0:nameid-format:"

        ## The interpretation is left to individual implementations.
        UNSPECIFIED = "{}unspecified".format(_PREFIX)

        ## Indicates a form of an email address.
        EMAIL = "{}emailAddress".format(_PREFIX)

        ## Is in the form specified by the X.509 recommendation [XMLSig].
        X509 = "{}X509SubjectName".format(_PREFIX)

        ## Is in the format of a Windows domain qualified name.
        WINDOWS = "{}WindowsDomainQualifiedName".format(_PREFIX)

        ## Is in the form of a Kerberos principal name.
        KEREBOS = "{}kerberos".format(_PREFIX)

        ## Is the identifier of an entity that provides SAML-based services.
        ENTITY = "{}entity".format(_PREFIX)

        ## Is a persistent opaque identifier for a principal.
        PERSISTENT = "{}persistent".format(_PREFIX)

        ## Is an identifier with transient semantics.
        TRANSIENT = "{}transient".format(_PREFIX)

    ## A URI classification of string-based identifier information.
    format = attribute.Attribute("Format", default=Format.UNSPECIFIED)

    ## A name identifier established by a service provider.
    sp_provided_id = attribute.Attribute("SPProvidedID")


class NameID(NameIDType):
    """Is the identifier used in various SAML assertion constructs."""
    pass


## \todo Element : <EncryptedID>
## \todo Type    : EncryptedElementType


class Issuer(NameIDType):
    """Represents the issuer of a SAML assertion or protocol message.
    """

    ## If no Format value is provided, then the value ENTITY is in effect.
    format = attribute.Attribute("Format", default=NameID.Format.ENTITY)


## \todo Element    : <AssertionIDRef>
## \todo Element    : <AssertionURIRef>


class SubjectConfirmationData(Element):
    """Specifies constraints on allowing a subject to be confirmed.
    """

    ## \todo Support for KeyInfoConfirmationDataType

    ## \todo Support for arbitrary attribute.Attributes
    ## \todo Support for arbitrary elements

    ## A time instant before which the subject cannot be confirmed.
    not_before = attribute.DateTimeAttribute("NotBefore")

    ## A time instant at which the subject can no longer be confirmed.
    not_on_or_after = attribute.DateTimeAttribute("NotOnOrAfter")

    ## URI specifying to which an attesting entity can present the assertion.
    recipient = attribute.Attribute("Recipient")

    ## ID of a SAML message to the entity can present the assertion to.
    in_response_to = attribute.Attribute("InResponseTo")

    ## The network address to which the saml entity can present the assertion.
    address = attribute.Attribute("Address")


class SubjectConfirmation(Element):
    """Provides the means for a relying party to verify the subject.
    """

    class Method:
        """Enumeration of known values."""

        ## URI namespace prefix of the values.
        _PREFIX = 'urn:oasis:names:tc:SAML:2.0:cm:'

        ## The subject is confirmed by the indicated data.
        BEARER = '{}bearer'.format(_PREFIX)

        ## The subject is confirmed by the holding of a key.
        HOLDER_OF_KEY = '{}holder-of-key'.format(_PREFIX)

    ## URI reference that identifies a protocol to confirm the subject.
    method = attribute.Attribute(
        name="Method",
        required=True,
        default=lambda: SubjectConfirmation.Method.BEARER)

    ## Identifies the entity expected to satisfy the enclosed requirements.
    id = BaseIDAbstractType()

    ## Confirmation information and constraints.
    data = SubjectConfirmationData(meta__index=1)


class Subject(Element):
    """The principal that is the subject of all statements in an assertion.
    """

    ## Identifies the subject.
    id = BaseIDAbstractType()

    ## Information that allows the subject to be confirmed.
    confirm = SubjectConfirmation(meta__index=1)


## \todo Element <EncryptedAssertion>
## \todo Element <Condition>
## \todo Elements <AudienceRestriction> and <Audience>
## \todo Element <OneTimeUse>
## \todo Element <ProxyRestriction>
## \todo Element <Advice>


class Statement(Element):
    """An extension point for statements made about a subject.
    """


class AuthenticationContext(Element):
    """Specifies the context of an authentication event.
    """

    class Meta(Element.Meta):
        name = 'AuthnContext'

    class Reference:
        """List of context classes defined by reference in SAML2.
        """

        ## URI prefix for the values in this enumeration.
        _PREFIX = "urn:oasis:names:tc:SAML:2.0:ac:classes:"

        ## Authenticated through the use of a provided IP address.
        INTERNET_PROTOCOL = "{}InternetProtocol".format(_PREFIX)

        ## Authenticated through a provided IP address and username/password.
        INTERNET_PROTOCOL_PASSWORD = "{}InternetProtocolPassword".format(
            _PREFIX)

        ## Authenticated using a Kerberos ticket.
        KERBEROS = "{}Kerberos".format(_PREFIX)

        ## Reflects no mobile customer registration procedures and an
        ## authentication of the mobile device without requiring explicit
        ## end-user interaction.
        MOBILE_ONE_FACTOR_UNREGISTERED = (
            "{}MobileOneFactorUnregistered".format(_PREFIX))

        ## Reflects no mobile customer registration procedures and a
        ## two-factor based authentication, such as secure device and user PIN.
        MOBILE_TWO_FACTOR_UNREGISTERED = (
            "{}MobileTwoFactorUnregistered".format(_PREFIX))

        ## Reflects mobile contract customer registration procedures and a
        ## single factor authentication.
        MOBILE_ONE_FACTOR_CONTRACT = "{}MobileOneFactorContract".format(
            _PREFIX)

        ## Reflects mobile contract customer registration procedures and a
        ## two-factor based authentication.
        MOBILE_TWO_FACTOR_CONTRACT = "{}MobileTwoFactorContract".format(
            _PREFIX)

        ## Authenticates through the presentation of a password over an
        ## unprotected HTTP session.
        PASSWORD = "{}Password".format(_PREFIX)

        ## Authentication through the presentation of a password over a
        ## protected session.
        PASSWORD_PROTECTED_TRANSPORT = "{}PasswordProtectedTransport".format(
            _PREFIX)

        ## A principal had authenticated to an authentication authority at
        ## some point in the past using any authentication context supported
        ## by that authentication authority.
        PREVIOUS_SESSION = "{}PreviousSession".format(_PREFIX)

        ## The principal authenticated by means of a digital signature where
        ## the key was validated as part of an X.509 Public Key Infrastructure.
        X509 = "{}X509".format(_PREFIX)

        ## The principal authenticated by means of a digital signature where
        ## key was validated as part of a PGP Public Key Infrastructure.
        PGP = "{}PGP".format(_PREFIX)

        ## The principal authenticated by means of a digital signature where
        ## the key was validated via an SPKI Infrastructure.
        SPKI = "{}SPKI".format(_PREFIX)

        ## This context class indicates that the principal authenticated by
        ## means of a digital signature according to the processing rules
        ## specified in the XML Digital Signature specification [XMLSig].
        XMLDSIG = "{}XMLDSig".format(_PREFIX)

        ## A principal authenticates to an authentication authority using a
        ## smartcard.
        SMARTCARD = "{}Smartcard".format(_PREFIX)

        ## A principal authenticates to an authentication authority through
        ## a two-factor authentication mechanism using a smartcard with
        ## enclosed private key and a PIN.
        SMARTCARD_PKI = "{}SmartcardPKI".format(_PREFIX)

        ## A principal uses an X.509 certificate stored in software to
        ## authenticate to the authentication authority.
        SOFTWARE_PKI = "{}SoftwarePKI".format(_PREFIX)

        ## The principal authenticated via the provision of a fixed-line
        ## telephone number, transported via a telephony protocol such as ADSL.
        TELEPHONY = "{}Telephony".format(_PREFIX)

        ## The principal is "roaming" (perhaps using a phone card) and
        ## authenticates via the means of the line number, a user suffix,
        ## and a password element.
        NOMAD_TELEPHONY = "{}NomadTelephony".format(_PREFIX)

        ## The principal authenticated via the provision of a fixed-line
        ## telephone number and a user suffix, transported via a telephony
        ## protocol such as ADSL.
        PERSONAL_TELEPHONY = "{}PersonalTelephony".format(_PREFIX)

        ## Authenticated via the means of the line number,
        ## a user suffix, and a password element.
        AUTHENTICATED_TELEPHONY = "{}AuthenticatedTelephony".format(_PREFIX)

        ## Authenticated by means of Secure Remote Password s[RFC 2945].
        SECURE_REMOTE_PASSWORD = "{}SecureRemotePassword".format(_PREFIX)

        ## The principal authenticated by means of a client certificate,
        ## secured with the SSL/TLS transport.
        TLS_CLIENT = "{}TLSClient".format(_PREFIX)

        ## A principal authenticates through a time synchronization token.
        TIME_SYNC_TOKEN = "{}TimeSyncToken".format(_PREFIX)

        ## Indicates that the authentication means are unspecified.
        UNSPECIFIED = "{}Unspecified".format(_PREFIX)

    ## A URI reference identifying an authentication context class that
    ## describes the authentication context declaration that follows.
    reference = element.Simple(
        name="AuthnContextClassRef",
        namespace=Meta.namespace,
        default=lambda: AuthenticationContext.Reference.UNSPECIFIED)


class AuthenticationStatement(Statement):
    """
    Describes a statement by the SAML authority asserting that the assertion
    subject was authenticated by a particular means at a particular time.
    """

    class Meta(Statement.Meta):
        name = 'AuthnStatement'

    ## Specifies the time at which the authentication took place.
    instant = attribute.DateTimeAttribute(
        name="AuthnInstant",
        required=True,
        default=datetime.utcnow)

    ## Specifies the index of a particular session between the principal
    ## identified by the subject and the authenticating authority.
    session_index = attribute.Attribute("SessionIndex")

    ## Specifies a time instant at which the session between the principal
    ## identified by the subject and the SAML authority issuing this
    ## statement MUST be considered ended.
    session_not_on_or_after = attribute.DateTimeAttribute(
        "SessionNotOnOrAfter")

    ## \todo <SubjectLocality>

    ## The context used by the authenticating authority up to and including
    ## the authentication event that yielded this statement.
    context = AuthenticationContext()


class Message(Element):
    """Specifies common information found in all SAML message."""

    ## \todo Element <ds:Signature>

    ## The version of the schema used by this assertion.
    version = attribute.Attribute(
        name="Version",
        required=True,
        default=VERSION)

    ## The identifier for this assertion.
    id = attribute.Attribute(
        name="ID",
        required=True,
        default=lambda: '_{}'.format(uuid4().hex))

    ## The time instant of issue, in UTC, for this assertion.
    issue_instant = attribute.Attribute(
        name="IssueInstant",
        required=True,
        default=datetime.utcnow)

    ## The SAML authority that is making the claim(s) in the assertion.
    issuer = Issuer(meta__min_occurs=1)


class Assertion(Message):
    """Specifies the basic information that is common to all assertions.
    """

    ## The subject of the statement(s) in the assertion.
    subject = Subject()

    ## \todo Element <Conditions>
    ## \todo Element <Advice>

    ## The collection of statements asserted by this assertion.
    statements = Statement(meta__index=1, meta__max_occurs=None)


## \todo Element <SubjectLocality>
## \todo Element <AttributeStatement>
## \todo Element <Attribute>
## \todo Element <AttributeValue>
## \todo Element <EncryptedAttribute>
## \todo Element <AuthzDecisionStatement>
## \todo Simple Type DecisionType
## \todo Element <Action>
## \todo Element <Evidence>
