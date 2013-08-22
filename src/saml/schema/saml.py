from uuid import uuid4
from datetime import datetime
from . import types, base, VERSION, Attribute, Element


class Base(base.Base):

    class Meta:
        namespace = 'saml', 'urn:oasis:names:tc:SAML:2.0:assertion'


class BaseID(Base):
    """Provides an extension point for identifiers.
    """

    #! The security or administrative domain that qualifies the name.
    name_qualifier = Attribute(types.String)

    #! Further qualifies a name with the name of a service provider.
    sp_name_qualifier = Attribute(types.String, name="SPNameQualifier")


class NameID(Base):
    """
    Is the identifier used in various SAML assertion
    constructs [saml-core § 2.2.3].
    """

    class Format:
        #! URI prefix for the values in this enumeration.
        _PREFIX = "urn:oasis:names:tc:SAML:2.0:nameid-format:"

        #! The interpretation is left to individual implementations.
        UNSPECIFIED = "{}unspecified".format(_PREFIX)

        #! Indicates a form of an email address.
        EMAIL = "{}emailAddress".format(_PREFIX)

        #! Is in the form specified by the X.509 recommendation [XMLSig].
        X509 = "{}X509SubjectName".format(_PREFIX)

        #! Is in the format of a Windows domain qualified name.
        WINDOWS = "{}WindowsDomainQualifiedName".format(_PREFIX)

        #! Is in the form of a Kerberos principal name.
        KEREBOS = "{}kerberos".format(_PREFIX)

        #! Is the identifier of an entity that provides SAML-based services.
        ENTITY = "{}entity".format(_PREFIX)

        #! Is a persistent opaque identifier for a principal.
        PERSISTENT = "{}persistent".format(_PREFIX)

        #! Is an identifier with transient semantics.
        TRANSIENT = "{}transient".format(_PREFIX)

    #! A URI classification of string-based identifier information.
    format = Attribute(types.String)

    #! A name identifier established by a service provider.
    sp_provided_id = Attribute(types.String, name="SPProvidedID")


class Issuer(NameID):
    """
    Represents the issuer of a SAML assertion or protocol
    message [saml-core § 2.2.5].
    """

    #! If no Format value is provided, then the value ENTITY is in effect.
    format = Attribute(types.String)


class _Message(Base):
    """Contains common information found in most SAML/2.0 communications.
    """

    #! The version of this message.
    version = Attribute(types.String, default=VERSION, required=True)

    #! The identifier for this message.
    id = Attribute(types.String, name='ID', required=True,
                   default=lambda: '_%s' % uuid4().hex)

    #! The time instant of issue in UTC.
    issue_instant = Attribute(types.DateTime, required=True,
                              default=datetime.utcnow)

    #! The SAML authority that is making the claim(s) in the message.
    issuer = Element(Issuer, required=True)


class Statement(Base):
    """An extension point for statements made about a subject.
    """


class AuthenticationContextReference(Statement):
    """
    A URI reference identifying an authentication context class that
    describes the authentication context declaration that follows.
    """

    class Meta:
        name = 'AuthnContextClassRef'

    #! URI prefix for the values in this enumeration.
    _PREFIX = "urn:oasis:names:tc:SAML:2.0:ac:classes:"

    #! Authenticated through the use of a provided IP address.
    INTERNET_PROTOCOL = "{}InternetProtocol".format(_PREFIX)

    #! Authenticated through a provided IP address and username/password.
    INTERNET_PROTOCOL_PASSWORD = "{}InternetProtocolPassword".format(
        _PREFIX)

    #! Authenticated using a Kerberos ticket.
    KERBEROS = "{}Kerberos".format(_PREFIX)

    #! Reflects no mobile customer registration procedures and an
    #! authentication of the mobile device without requiring explicit
    #! end-user interaction.
    MOBILE_ONE_FACTOR_UNREGISTERED = (
        "{}MobileOneFactorUnregistered".format(_PREFIX))

    #! Reflects no mobile customer registration procedures and a
    #! two-factor based authentication, such as secure device and user PIN.
    MOBILE_TWO_FACTOR_UNREGISTERED = (
        "{}MobileTwoFactorUnregistered".format(_PREFIX))

    #! Reflects mobile contract customer registration procedures and a
    #! single factor authentication.
    MOBILE_ONE_FACTOR_CONTRACT = "{}MobileOneFactorContract".format(
        _PREFIX)

    #! Reflects mobile contract customer registration procedures and a
    #! two-factor based authentication.
    MOBILE_TWO_FACTOR_CONTRACT = "{}MobileTwoFactorContract".format(
        _PREFIX)

    #! Authenticates through the presentation of a password over an
    #! unprotected HTTP session.
    PASSWORD = "{}Password".format(_PREFIX)

    #! Authentication through the presentation of a password over a
    #! protected session.
    PASSWORD_PROTECTED_TRANSPORT = "{}PasswordProtectedTransport".format(
        _PREFIX)

    #! A principal had authenticated to an authentication authority at
    #! some point in the past using any authentication context supported
    #! by that authentication authority.
    PREVIOUS_SESSION = "{}PreviousSession".format(_PREFIX)

    #! The principal authenticated by means of a digital signature where
    #! the key was validated as part of an X.509 Public Key Infrastructure.
    X509 = "{}X509".format(_PREFIX)

    #! The principal authenticated by means of a digital signature where
    #! key was validated as part of a PGP Public Key Infrastructure.
    PGP = "{}PGP".format(_PREFIX)

    #! The principal authenticated by means of a digital signature where
    #! the key was validated via an SPKI Infrastructure.
    SPKI = "{}SPKI".format(_PREFIX)

    #! This context class indicates that the principal authenticated by
    #! means of a digital signature according to the processing rules
    #! specified in the XML Digital Signature specification [XMLSig].
    XMLDSIG = "{}XMLDSig".format(_PREFIX)

    #! A principal authenticates to an authentication authority using a
    #! smartcard.
    SMARTCARD = "{}Smartcard".format(_PREFIX)

    #! A principal authenticates to an authentication authority through
    #! a two-factor authentication mechanism using a smartcard with
    #! enclosed private key and a PIN.
    SMARTCARD_PKI = "{}SmartcardPKI".format(_PREFIX)

    #! A principal uses an X.509 certificate stored in software to
    #! authenticate to the authentication authority.
    SOFTWARE_PKI = "{}SoftwarePKI".format(_PREFIX)

    #! The principal authenticated via the provision of a fixed-line
    #! telephone number, transported via a telephony protocol such as ADSL.
    TELEPHONY = "{}Telephony".format(_PREFIX)

    #! The principal is "roaming" (perhaps using a phone card) and
    #! authenticates via the means of the line number, a user suffix,
    #! and a password element.
    NOMAD_TELEPHONY = "{}NomadTelephony".format(_PREFIX)

    #! The principal authenticated via the provision of a fixed-line
    #! telephone number and a user suffix, transported via a telephony
    #! protocol such as ADSL.
    PERSONAL_TELEPHONY = "{}PersonalTelephony".format(_PREFIX)

    #! Authenticated via the means of the line number,
    #! a user suffix, and a password element.
    AUTHENTICATED_TELEPHONY = "{}AuthenticatedTelephony".format(_PREFIX)

    #! Authenticated by means of Secure Remote Password s[RFC 2945].
    SECURE_REMOTE_PASSWORD = "{}SecureRemotePassword".format(_PREFIX)

    #! The principal authenticated by means of a client certificate,
    #! secured with the SSL/TLS transport.
    TLS_CLIENT = "{}TLSClient".format(_PREFIX)

    #! A principal authenticates through a time synchronization token.
    TIME_SYNC_TOKEN = "{}TimeSyncToken".format(_PREFIX)

    #! Indicates that the authentication means are unspecified.
    UNSPECIFIED = "{}Unspecified".format(_PREFIX)


class AuthenticationContext(Base):
    """Specifies the context of an authentication event.
    """

    class Meta:
        name = 'AuthnContext'

    #! A URI reference identifying an authentication context class that
    #! describes the authentication context declaration that follows.
    reference = Element(AuthenticationContextReference,
                        default=AuthenticationContextReference.UNSPECIFIED)

    # TODO: <AuthnContextDecl> or <AuthnContextDeclRef>
    # TODO: <AuthenticatingAuthority>


class SubjectLocality(Base):
    """
    Specifies the DNS domain name and IP address for the system from
    which the assertion subject was authenticated.
    """


class AuthenticationStatement(Statement):
    """
    Describes a statement by the SAML authority asserting that the assertion
    subject was authenticated by a particular means at a particular time.
    """

    class Meta:
        name = 'AuthnStatement'

    #! Specifies the time at which the authentication took place.
    authn_instant = Attribute(types.DateTime, required=True,
                              default=datetime.utcnow)

    #! Specifies the index of a particular session between the principal
    #! identified by the subject and the authenticating authority.
    session_index = Attribute(types.String)

    #! Specifies a time instant at which the session between the principal
    #! identified by the subject and the SAML authority issuing this
    #! statement MUST be considered ended.
    session_not_on_or_after = Attribute(types.DateTime)

    #! Specifies the DNS domain name and IP address for the system from which
    #! the assertion subject was apparently authenticated.
    subject_locality = Element(SubjectLocality)

    #! The context used by the authenticating authority up to and including
    #! the authentication event that yielded this statement.
    context = Element(AuthenticationContext)


class SubjectConfirmationData(Base):
    """Specifies constraints on allowing a subject to be confirmed.
    """

    # TODO: <KeyInfoConfirmationDataType/>
    # TODO: Arbitrary attributes
    # TODO: Arbitrary elements

    #! A time instant before which the subject cannot be confirmed.
    not_before = Attribute(types.DateTime)

    #! A time instant at which the subject can no longer be confirmed.
    not_on_or_after = Attribute(types.DateTime)

    #! URI specifying to which an attesting entity can present the assertion.
    recipient = Attribute(types.String)

    #! ID of a SAML message to the entity can present the assertion to.
    in_response_to = Attribute(types.String)

    #! The network address to which the saml entity can present the assertion.
    address = Attribute(types.String)


class SubjectConfirmation(Base):
    """
    Provides the means for a relying party to verify the
    correspondence of the subject of the assertion with the party with whom
    the relying party is communicating.
    """

    class Method:

        #! URI namespace prefix of the values.
        _PREFIX = 'urn:oasis:names:tc:SAML:2.0:cm:'

        #! The subject is confirmed by the indicated data.
        BEARER = '{}bearer'.format(_PREFIX)

        #! The subject is confirmed by the holding of a key.
        HOLDER_OF_KEY = '{}holder-of-key'.format(_PREFIX)

    #! URI reference that identifies a protocol to confirm the subject.
    method = Attribute(types.String, required=True, default=Method.BEARER)

    #! Identifies the entity expected to satisfy the enclosed requirements.
    id = Element(NameID)

    #! Confirmation information and constraints.
    data = Element(SubjectConfirmationData)


class Subject(Base):
    """The principal that is the subject of all statements in an assertion.
    """

    #! Identifies the subject.
    id = Element(NameID)

    #! Information that allows the subject to be confirmed. If more than one
    #! subject confirmation is provided, then satisfying any one of them is
    #! sufficient to confirm the subject for the purpose of applying
    #! the assertion.
    confirmation = Element(SubjectConfirmation, collection=True)


class Condition(Base):
    """Serves as an extension point for new conditions.
    """


class Conditions(Base):
    """
    Defines the SAML constructs that place constraints on the
    acceptable use of SAML assertions.
    """

    #! A time instant before which the subject cannot be confirmed.
    not_before = Attribute(types.DateTime)

    #! A time instant at which the subject can no longer be confirmed.
    not_on_or_after = Attribute(types.DateTime)

    #! Specifies that the assertion is addressed to a particular audience.
    condition = Element(Condition, collection=True)


class Audience(Base):
    """A URI reference that identifies an intended audience.
    """


class AudienceRestriction(Condition):
    """
    Specifies that the assertion is addressed to one or more
    specific audiences.
    """

    audiences = Element(Audience, collection=True)


class OneTimeUse(Condition):
    """
    Allows an authority to indicate that the information
    in the assertion is likely to change very soon and fresh information
    should be obtained for each use.
    """


class Assertion(_Message):
    """
    This type specifies the basic information that is common to
    all assertions [saml-core § 2.3.3].
    """

    #! The subject of the statement(s) in the assertion.
    subject = Element(Subject)

    #! Conditions that MUST be evaluated when assessing the validity
    #! of and/or when using the assertion.
    conditions = Element(Conditions)

    #! Additional information related to the assertion that assists
    #! processing in certain situations but which MAY be ignored by
    #! applications that do not understand the advice or do not wish to
    #! make use of it.
    # TODO: <Advice/>

    #! Statements that are being asserted about the included subject.
    statements = Element(Statement, collection=True)
