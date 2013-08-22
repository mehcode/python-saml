from . import types, base, Attribute, Element, saml


class Base(base.Base):

    class Meta:
        namespace = 'samlp', 'urn:oasis:names:tc:SAML:2.0:protocol'


class _Message(saml._Message, Base):
    """Contains common information found in most SAML/2.0 protocols.
    """

    #! A URI reference indicating the address to which this request has
    #! been sent.
    destination = Attribute(types.String)

    #! Indicates whether or not (and under what conditions) consent has
    #! been obtained from a principal in the sending of this request.
    consent = Attribute(types.String)


class NameIDPolicy(Base):
    """
    Tailors the name identifier in the subjects of assertions
    resulting from an <AuthnRequest>.
    """

    #! Specifies the URI reference corresponding to a name identifier format
    #! defined in this or another specification.
    format = Attribute(types.String)

    #! Optionally specifies that the assertion subject's identifier be
    #! returned (or created) in the namespace of a service provider
    #! other than the requester, or in the namespace of an affiliation
    #! group of service providers
    sp_name_qualifier = Attribute(types.String, name='SPNameQualifier')

    #! A Boolean value used to indicate whether the identity provider is
    #! allowed, in the course of fulfilling the request, to create a
    #! new identifier to represent the principal.
    allow_create = Attribute(types.Boolean)


class RequestedAuthenticationContext(Base):

    class Meta:
        name = 'RequestedAuthnContext'

    #! Specifies the comparison method used to evaluate the requested
    #! context classes or statements, one of "exact", "minimum",
    #! "maximum", or "better". The default is "exact".
    comparison = Attribute(types.String)

    #! Specifies one or more URI references identifying authentication
    #! context classes or declarations.
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

    class Meta:
        name = 'AuthnRequest'

    #! A Boolean value. If "true", the identity provider MUST authenticate
    #! the presenter directly rather than rely on a previous security context.
    force_authn = Attribute(types.Boolean)

    #! A Boolean value. If "true", the identity provider and the user agent
    #! itself MUST NOT visibly take control of the user interface from the
    #! requester and interact with the presenter in a noticeable fashion.
    is_passive = Attribute(types.Boolean)

    #! A URI reference that identifies a SAML protocol binding to be used when
    #! returning the <Response> message.
    protocol = Attribute(types.String, name='ProtocolBinding')

    #! Indirectly identifies the location to which the <Response> message
    #! should be returned to the requester.
    assertion_consumer_service_index = Attribute(types.Integer)

    #! Specifies by value the location to which the <Response> message MUST
    #! be returned to the requester.
    assertion_consumer_service_url = Attribute(
        types.String, name='AssertionConsumerServiceURL')

    #! Indirectly identifies information associated with the requester
    #! describing the SAML attributes the requester desires or requires to be
    #! supplied by the identity provider in the <Response> message.
    attribute_consuming_service_index = Attribute(types.Integer)

    #! Specifies the human-readable name of the requester for use by the
    #! presenter's user agent or the identity provider.
    provider_name = Attribute(types.String)

    #! Specifies the requested subject of the resulting assertion(s).
    subject = Element(saml.Subject)

    #! Specifies constraints on the name identifier to be used to represent
    #! the requested subject.
    policy = Element(NameIDPolicy)

    #! Specifies the requirements, if any, that the requester places on
    #! the authentication context that applies to the responding provider's
    #! authentication of the presenter.
    requested_context = Element(RequestedAuthenticationContext)

    #! Specifies a set of identity providers trusted by the requester to
    #! authenticate the presenter, as well as limitations and context
    #! related to proxying of the <AuthnRequest> message to subsequent identity
    #! providers by the responder.
    # TODO: scoping = Element(Scoping)


class StatusCode(Base):

    #! URI prefix for the values in this enumeration.
    _PREFIX = "urn:oasis:names:tc:SAML:2.0:status:"

    #! The request succeeded.
    SUCCESS = "{}Success".format(_PREFIX)

    #! Failure due to an error on the part of the requester.
    REQUESTER = "{}Requester".format(_PREFIX)

    #! The version of the request message was incorrect.
    VERSION_MISMATCH = "{}VersionMismatch".format(_PREFIX)

    #! The provider wasn't able to successfully authenticate the principal.
    AUTHENTICATION_FAILED = "{}AuthnFailed".format(_PREFIX)

    #! Unexpected or invalid content was encountered.
    INVALID_ATTRIBUTE_NAME_OR_VALUE = "{}InvalidAttrNameOrValue".format(
        _PREFIX)

    #! The responding provider cannot support the requested name ID policy.
    INVALID_NAME_ID_POLICY = "{}InvalidNameIDPolicy".format(_PREFIX)

    #! The authentication context requirements cannot be met.
    NO_AUTHENTICATION_CONTEXT = "{}NoAuthnContext".format(_PREFIX)

    #! None of the supported identity providers are available.
    NO_AVAILABLE_IDP = "{}NoAvailableIDP".format(_PREFIX)

    #! The responding provider cannot authenticate the principal passively.
    NO_PASSIVE = "{}NoPassive".format(_PREFIX)

    #! None of the identity providers are supported by the intermediary.
    NO_SUPPORTED_IDP = "{}NoSupportedIDP".format(_PREFIX)

    #! Not able to propagate logout to all other session participants.
    PARTIAL_LOGOUT = "{}PartialLogout".format(_PREFIX)

    #! Cannot authenticate directly and not permitted to proxy the request.
    PROXY_COUNT_EXCEEDED = "{}ProxyCountExceeded".format(_PREFIX)

    #! Is able to process the request but has chosen not to respond.
    REQUEST_DENIED = "{}RequestDenied".format(_PREFIX)

    #! The SAML responder or SAML authority does not support the request.
    REQUEST_UNSUPPORTED = "{}RequestUnsupported".format(_PREFIX)

    #! Deprecated protocol version specified in the request.
    REQUEST_VERSION_DEPRECATED = "{}RequestVersionDeprecated".format(
        _PREFIX)

    #! Protocol version specified in the request message is too low.
    REQUEST_VERSION_TOO_LOW = "{}RequestVersionTooHigh".format(_PREFIX)

    #! Protocol version specified in the request message is too high.
    REQUEST_VERSION_TOO_HIGH = "{}RequestVersionTooLow".format(_PREFIX)

    #! Resource value provided in the request message is invalid.
    RESOURCE_NOT_RECOGNIZED = "{}ResourceNotRecognized".format(_PREFIX)

    #! The response message would contain more elements than able.
    TOO_MANY_RESPONSES = "{}TooManyResponses".format(_PREFIX)

    #! Attribute from an unknown attribute profile.
    UNKNOWN_ATTR_PROFILE = "{}UnknownAttrProfile".format(_PREFIX)

    #! The responder does not recognize the principal.
    UNKNOWN_PRINCIPAL = "{}UnknownPrincipal".format(_PREFIX)

    #! The SAML responder cannot properly fulfill the request.
    UNSUPPORTED_BINDING = "{}UnsupportedBinding".format(_PREFIX)

    #! The status code value. This attribute contains a URI reference.
    value = Attribute(types.String)

    #! A subordinate status code that provides more specific information
    #! on an error condition.
    # TODO: code = Element('self')


class Status(Base):

    #! A code representing the status of the activity carried out in
    #! response to the corresponding request.
    code = Element(StatusCode, required=True)


class StatusResponse(_Message):
    """Extends the common message type with a status element.
    """

    #! A reference to the identifier of the request to which the
    #! response corresponds, if any.
    in_response_to = Attribute(types.String)

    #! A code representing the status of the corresponding request.
    status = Element(Status)


class Response(StatusResponse):
    """
    Used when a response consists of a list of zero or more assertions
    that satisfy the request.
    """

    #! Specifies an assertion by value, or optionally an encrypted assertion
    #! by value.
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

    #! The artifact value that the requester received and now wishes to
    #! translate into the protocol message it represents.
    artifact = Element(Artifact, required=True)


class ArtifactResponse(StatusResponse):
    """
    Responds to an <ArtifactResolve> request with an embedded message
    that was referenced by the given artifact.
    """

    #! The embedded message.
    message = Element(_Message)
