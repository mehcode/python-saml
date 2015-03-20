# -*- coding: utf-8 -*-
from . import types, base, Element, saml


class Base(base.Base):

    class Meta:
        namespace = 'samlp', 'urn:oasis:names:tc:SAML:2.0:protocol'


class _Message(saml._Message, Base):
    """Contains common information found in most SAML/2.0 protocols.
    """

    # A URI reference indicating the address to which this request has
    # been sent.
    destination = base.Attribute(types.String)

    # Indicates whether or not (and under what conditions) consent has
    # been obtained from a principal in the sending of this request.
    consent = base.Attribute(types.String)


class NameIDPolicy(Base):
    """
    Tailors the name identifier in the subjects of assertions
    resulting from an <AuthnRequest>.
    """

    # Specifies the URI reference corresponding to a name identifier format
    # defined in this or another specification.
    format = base.Attribute(types.String)

    # Optionally specifies that the assertion subject's identifier be
    # returned (or created) in the namespace of a service provider
    # other than the requester, or in the namespace of an affiliation
    # group of service providers
    sp_name_qualifier = base.Attribute(types.String, name='SPNameQualifier')

    # A Boolean value used to indicate whether the identity provider is
    # allowed, in the course of fulfilling the request, to create a
    # new identifier to represent the principal.
    allow_create = base.Attribute(types.Boolean)


class RequestedAuthenticationContext(Base):

    class Meta:
        name = 'RequestedAuthnContext'

    # Specifies the comparison method used to evaluate the requested
    # context classes or statements, one of "exact", "minimum",
    # "maximum", or "better". The default is "exact".
    comparison = base.Attribute(types.String)

    # Specifies one or more URI references identifying authentication
    # context classes or declarations.
    reference = Element(saml.AuthenticationContextReference, collection=True)


class Protocol:
    """
    The available URIs that identifies a SAML protocol binding to be used when
    returning the <Response> message.
    """

    _PREFIX = 'urn:oasis:names:tc:SAML:2.0:bindings:'

    SOAP = '%sSOAP' % _PREFIX

    POAS = '%sPAOS' % _PREFIX

    REDIRECT = '%sHTTP-Redirect' % _PREFIX

    POST = '%sHTTP-POST' % _PREFIX

    ARTIFACT = '%sHTTP-Artifact' % _PREFIX

    URI = '%sURI' % _PREFIX


class AuthenticationRequest(_Message):
    """
    Create a SAML AuthnRequest
    ::
        from saml import schema
        from datetime import datetime

        document = schema.AuthenticationRequest()
        document.id = '11111111-2222-3333-4444-555555555555'
        document.issue_instant = datetime(2000, 1, 1)
        document.assertion_consumer_service_index = 0
        document.attribute_consuming_service_index = 0
        document.issuer = 'https://sp.example.com/SAML2'

        policy = schema.NameIDPolicy()
        policy.allow_create = True
        policy.format = schema.NameID.Format.TRANSIENT
        document.policy = policy

        print document.tostring()

    Produces the following XML document:

    .. code-block:: xml

        <samlp:AuthnRequest
            xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
            xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
            Version="2.0"
            ID="11111111-2222-3333-4444-555555555555"
            IssueInstant="2000-01-01T00:00:00Z"
            AssertionConsumerServiceIndex="0"
            AttributeConsumingServiceIndex="0">
            <saml:Issuer>https://sp.example.com/SAML2</saml:Issuer>
            <samlp:NameIDPolicy
                Format="urn:oasis:names:tc:SAML:2.0:nameid-format:transient"
                AllowCreate="true"/>
        </samlp:AuthnRequest>
    """

    class Meta:
        name = 'AuthnRequest'

    # A Boolean value. If "true", the identity provider MUST authenticate
    # the presenter directly rather than rely on a previous security context.
    force_authn = base.Attribute(types.Boolean)

    # A Boolean value. If "true", the identity provider and the user agent
    # itself MUST NOT visibly take control of the user interface from the
    # requester and interact with the presenter in a noticeable fashion.
    is_passive = base.Attribute(types.Boolean)

    # A URI reference that identifies a SAML protocol binding to be used when
    # returning the <Response> message.
    protocol = base.Attribute(types.String, name='ProtocolBinding')

    # Indirectly identifies the location to which the <Response> message
    # should be returned to the requester.
    assertion_consumer_service_index = base.Attribute(types.Integer)

    # Specifies by value the location to which the <Response> message MUST
    # be returned to the requester.
    assertion_consumer_service_url = base.Attribute(
        types.String, name='AssertionConsumerServiceURL')

    # Indirectly identifies information associated with the requester
    # describing the SAML attributes the requester desires or requires to be
    # supplied by the identity provider in the <Response> message.
    attribute_consuming_service_index = base.Attribute(types.Integer)

    # Specifies the human-readable name of the requester for use by the
    # presenter's user agent or the identity provider.
    provider_name = base.Attribute(types.String)

    # Specifies the requested subject of the resulting assertion(s).
    subject = Element(saml.Subject)

    # Specifies constraints on the name identifier to be used to represent
    # the requested subject.
    policy = Element(NameIDPolicy)

    # Specifies the requirements, if any, that the requester places on
    # the authentication context that applies to the responding provider's
    # authentication of the presenter.
    requested_context = Element(RequestedAuthenticationContext)

    # Specifies a set of identity providers trusted by the requester to
    # authenticate the presenter, as well as limitations and context
    # related to proxying of the <AuthnRequest> message to subsequent identity
    # providers by the responder.
    # TODO: scoping = Element(Scoping)


class StatusCode(Base):

    # URI prefix for the values in this enumeration.
    _PREFIX = "urn:oasis:names:tc:SAML:2.0:status:"

    # The request succeeded.
    SUCCESS = "{}Success".format(_PREFIX)

    # Failure due to an error on the part of the requester.
    REQUESTER = "{}Requester".format(_PREFIX)

    # The version of the request message was incorrect.
    VERSION_MISMATCH = "{}VersionMismatch".format(_PREFIX)

    # The provider wasn't able to successfully authenticate the principal.
    AUTHENTICATION_FAILED = "{}AuthnFailed".format(_PREFIX)

    # Unexpected or invalid content was encountered.
    INVALID_ATTRIBUTE_NAME_OR_VALUE = "{}InvalidAttrNameOrValue".format(
        _PREFIX)

    # The responding provider cannot support the requested name ID policy.
    INVALID_NAME_ID_POLICY = "{}InvalidNameIDPolicy".format(_PREFIX)

    # The authentication context requirements cannot be met.
    NO_AUTHENTICATION_CONTEXT = "{}NoAuthnContext".format(_PREFIX)

    # None of the supported identity providers are available.
    NO_AVAILABLE_IDP = "{}NoAvailableIDP".format(_PREFIX)

    # The responding provider cannot authenticate the principal passively.
    NO_PASSIVE = "{}NoPassive".format(_PREFIX)

    # None of the identity providers are supported by the intermediary.
    NO_SUPPORTED_IDP = "{}NoSupportedIDP".format(_PREFIX)

    # Not able to propagate logout to all other session participants.
    PARTIAL_LOGOUT = "{}PartialLogout".format(_PREFIX)

    # Cannot authenticate directly and not permitted to proxy the request.
    PROXY_COUNT_EXCEEDED = "{}ProxyCountExceeded".format(_PREFIX)

    # Is able to process the request but has chosen not to respond.
    REQUEST_DENIED = "{}RequestDenied".format(_PREFIX)

    # The SAML responder or SAML authority does not support the request.
    REQUEST_UNSUPPORTED = "{}RequestUnsupported".format(_PREFIX)

    # Deprecated protocol version specified in the request.
    REQUEST_VERSION_DEPRECATED = "{}RequestVersionDeprecated".format(
        _PREFIX)

    # Protocol version specified in the request message is too low.
    REQUEST_VERSION_TOO_LOW = "{}RequestVersionTooHigh".format(_PREFIX)

    # Protocol version specified in the request message is too high.
    REQUEST_VERSION_TOO_HIGH = "{}RequestVersionTooLow".format(_PREFIX)

    # Resource value provided in the request message is invalid.
    RESOURCE_NOT_RECOGNIZED = "{}ResourceNotRecognized".format(_PREFIX)

    # The response message would contain more elements than able.
    TOO_MANY_RESPONSES = "{}TooManyResponses".format(_PREFIX)

    # base.Attribute from an unknown attribute profile.
    UNKNOWN_ATTR_PROFILE = "{}UnknownAttrProfile".format(_PREFIX)

    # The responder does not recognize the principal.
    UNKNOWN_PRINCIPAL = "{}UnknownPrincipal".format(_PREFIX)

    # The SAML responder cannot properly fulfill the request.
    UNSUPPORTED_BINDING = "{}UnsupportedBinding".format(_PREFIX)

    # The status code value. This attribute contains a URI reference.
    value = base.Attribute(types.String)

    # A subordinate status code that provides more specific information
    # on an error condition.
    # TODO: code = Element('self')


class Status(Base):

    # A code representing the status of the activity carried out in
    # response to the corresponding request.
    code = Element(StatusCode, required=True)


class StatusResponse(_Message):
    """Extends the common message type with a status element.
    """

    # A reference to the identifier of the request to which the
    # response corresponds, if any.
    in_response_to = base.Attribute(types.String)

    # A code representing the status of the corresponding request.
    status = Element(Status)


class Response(StatusResponse):
    """
    Create a SAML Response
    ::
        from saml import schema
        from datetime import datetime

        document = schema.Response()
        document.id = '11111111-1111-1111-1111-111111111111'
        document.in_response_to = '22222222-2222-2222-2222-222222222222'
        document.issue_instant = datetime(2000, 1, 1, 1)
        document.issuer = 'https://idp.example.org/SAML2'
        document.destination = 'https://sp.example.com/SAML2/SSO/POST'
        document.status.code.value = schema.StatusCode.SUCCESS

        # Create an assertion for the response.
        document.assertions = assertion = schema.Assertion()
        assertion.id = '33333333-3333-3333-3333-333333333333'
        assertion.issue_instant = datetime(2000, 1, 1, 2)
        assertion.issuer = 'https://idp.example.org/SAML2'

        # Create a subject.
        assertion.subject = schema.Subject()
        assertion.subject.principal = '44444444-4444-4444-4444-444444444444'
        assertion.subject.principal.format = schema.NameID.Format.TRANSIENT
        data = schema.SubjectConfirmationData()
        data.in_response_to = '22222222-2222-2222-2222-222222222222'
        data.not_on_or_after = datetime(2000, 1, 1, 1, 10)
        data.recipient = 'https://sp.example.com/SAML2/SSO/POST'
        confirmation = schema.SubjectConfirmation()
        confirmation.data = data
        assertion.subject.confirmation = confirmation

        # Create an authentication statement.
        statement = schema.AuthenticationStatement()
        assertion.statements.append(statement)
        statement.authn_instant = datetime(2000, 1, 1, 1, 3)
        statement.session_index = '33333333-3333-3333-3333-333333333333'
        reference = schema.AuthenticationContextReference
        statement.context.reference = reference.PASSWORD_PROTECTED_TRANSPORT

        # Create a authentication condition.
        assertion.conditions = conditions = schema.Conditions()
        conditions.not_before = datetime(2000, 1, 1, 1, 3)
        conditions.not_on_or_after = datetime(2000, 1, 1, 1, 9)
        condition = schema.AudienceRestriction()
        condition.audiences = 'https://sp.example.com/SAML2'
        conditions.condition = condition

        print document.tostring()

    Produces the following XML document:

    .. code-block:: xml

        <samlp:Response
            xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
            xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
            Version="2.0"
            ID="11111111-1111-1111-1111-111111111111"
            IssueInstant="2000-01-01T01:00:00Z"
            Destination="https://sp.example.com/SAML2/SSO/POST"
            InResponseTo="22222222-2222-2222-2222-222222222222">
            <saml:Issuer>https://idp.example.org/SAML2</saml:Issuer>
            <samlp:Status>
                <samlp:StatusCode
                    Value="urn:oasis:names:tc:SAML:2.0:status:Success"/>
            </samlp:Status>
            <saml:Assertion
                Version="2.0"
                ID="33333333-3333-3333-3333-333333333333"
                IssueInstant="2000-01-01T02:00:00Z">
                <saml:Issuer>https://idp.example.org/SAML2</saml:Issuer>
                <saml:Subject>
                    <saml:NameID
                        Format=
                        "urn:oasis:names:tc:SAML:2.0:nameid-format:transient">
                        44444444-4444-4444-4444-444444444444
                    </saml:NameID>
                    <saml:SubjectConfirmation
                        Method="urn:oasis:names:tc:SAML:2.0:cm:bearer">
                        <saml:SubjectConfirmationData
                            NotOnOrAfter="2000-01-01T01:10:00Z"
                            Recipient="https://sp.example.com/SAML2/SSO/POST"
                            InResponseTo=
                            "22222222-2222-2222-2222-222222222222"/>
                    </saml:SubjectConfirmation>
                </saml:Subject>
                <saml:Conditions
                    NotBefore="2000-01-01T01:03:00Z"
                    NotOnOrAfter="2000-01-01T01:09:00Z">
                    <saml:AudienceRestriction>
                        <saml:Audience>
                            https://sp.example.com/SAML2
                        </saml:Audience>
                    </saml:AudienceRestriction>
                </saml:Conditions>
                <saml:AuthnStatement
                    AuthnInstant="2000-01-01T01:03:00Z"
                    SessionIndex="33333333-3333-3333-3333-333333333333">
                    <saml:AuthnContext>
                        <saml:AuthnContextClassRef>
                            urn:oasis:names:tc:SAML:2.0:ac:classes:
                            PasswordProtectedTransport
                        </saml:AuthnContextClassRef>
                    </saml:AuthnContext>
                </saml:AuthnStatement>
            </saml:Assertion>
        </samlp:Response>
    """

    # Specifies an assertion by value, or optionally an encrypted assertion
    # by value.
    assertions = Element(saml.Assertion, collection=True)


class Artifact(Base):
    """
    The artifact value that the requester received and now wishes to
    translate into the protocol message it represents.
    """


class ArtifactResolve(_Message):
    """
    Used to request that a SAML protocol message be returned in an
    <ArtifactResponse> message by specifying an artifact that represents
    the SAML protocol message.
    """

    # The artifact value that the requester received and now wishes to
    # translate into the protocol message it represents.
    artifact = Element(Artifact, required=True)


class ArtifactResponse(StatusResponse):
    """
    Responds to an <ArtifactResolve> request with an embedded message
    that was referenced by the given artifact.
    """

    # The embedded message.
    message = Element(_Message)


class SessionIndex(Base):
    """The identifier that indexes a session at the message recipient.
    """


class LogoutRequest(_Message):
    """
    Create a SAML LogoutRequest
    ::
        from saml import schema
        from datetime import datetime

        document = schema.LogoutRequest()
        document.id = '11111111-1111-1111-1111-111111111111'
        document.issue_instant = datetime(2000, 1, 1)
        document.issuer = 'https://idp.example.org/SAML2'
        document.destination = 'https://sp.example.org/SAML2/logout'
        document.principal = 'myemail@mydomain.com'
        document.principal.format = schema.NameID.Format.EMAIL
        document.principal.name_qualifier = 'https://idp.example.org/SAML2'
        document.session_index = 'SESSION-22222222-2222-2222-2222-222222222222'

        print document.tostring()

    Produces the following XML document:

    .. code-block:: xml

        <samlp:LogoutRequest
            xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
            xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
            Version="2.0"
            ID="11111111-1111-1111-1111-111111111111"
            IssueInstant="2000-01-01T00:00:00Z"
            Destination="https://idphost/adfs/ls/">
            <saml:Issuer>https://idp.example.org/SAML2</saml:Issuer>
            <saml:NameID
                NameQualifier="https://idp.example.org/SAML2"
                Format="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress">
                myemail@mydomain.com
            </saml:NameID>
            <samlp:SessionIndex>
                SESSION-22222222-2222-2222-2222-222222222222
            </samlp:SessionIndex>
        </samlp:LogoutRequest>
    """

    # The time at which the request expires, after which the recipient
    # may discard the message.
    not_on_or_after = base.Attribute(types.DateTime)

    # An indication of the reason for the logout, in the
    # form of a URI reference.
    reason = base.Attribute(types.String)

    # The identifier and associated attributes
    # (in plaintext or encrypted form) that specify the principal as
    # currently recognized by the identity and service providers prior
    # to this request.
    principal = Element(saml.NameID, required=True)

    # The identifier that indexes this session at the message recipient.
    session_index = Element(SessionIndex)


class LogoutResponse(StatusResponse):
    """
    Create a SAML LogoutResponse
    ::
        from saml import schema
        from datetime import datetime

        document = schema.LogoutResponse()
        document.id = '22222222-2222-2222-2222-222222222222'
        document.in_response_to = '11111111-1111-1111-1111-111111111111'
        document.issue_instant = datetime(2000, 1, 1)
        document.issuer = 'https://idp.example.org/SAML2'
        document.destination = 'https://sp.example.com/SAML2/SLO/POST'
        document.status.code.value = schema.StatusCode.SUCCESS

        print document.tostring()

    Produces the following XML document:

    .. code-block:: xml

        <samlp:LogoutResponse
            xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
            xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
            Version="2.0"
            ID="22222222-2222-2222-2222-222222222222"
            IssueInstant="2000-01-01T00:00:00Z"
            Destination="https://sp.example.com/SAML2/SLO/POST"
            InResponseTo="11111111-1111-1111-1111-111111111111">
            <saml:Issuer>https://idp.example.org/SAML2</saml:Issuer>
            <samlp:Status>
                <samlp:StatusCode
                    Value="urn:oasis:names:tc:SAML:2.0:status:Success"/>
            </samlp:Status>
        </samlp:LogoutResponse>
    """
