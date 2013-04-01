# -*- coding: utf-8 -*-
"""Defines the XML data types for SAML2 in the samlp namespace.
"""
from . import saml
from . import attribute, element


class Element(element.Element):
    class Meta(element.Element.Meta):
        namespace = ("samlp", "urn:oasis:names:tc:SAML:2.0:protocol")


class Message(saml.Message):
    """Specifies commonalities that are associated with all SAML protocols.
    """

    class Meta(saml.Message.Meta):
        namespace = Element.Meta.namespace

    ## URI reference indicating h this message has been sent.
    destination = attribute.Attribute("Destination")

    ## Indicates how consent has been obtained from a principal.
    consent = attribute.Attribute("Consent")

    ## \todo Element <Extensions>


## \todo Element <StatusDetail>


class StatusCode(Element):
    """ Specifies a code or a set of nested codes representing the status.
    """

    class Value:
        """Enumeration of possible values."""

        ## URI prefix for the values in this enumeration.
        _PREFIX = "urn:oasis:names:tc:SAML:2.0:status:"

        ## The request succeeded.
        SUCCESS = "{}Success".format(_PREFIX)

        ## Failure due to an error on the part of the requester.
        REQUESTER = "{}Requester".format(_PREFIX)

        ## The version of the request message was incorrect.
        VERSION_MISMATCH = "{}VersionMismatch".format(_PREFIX)

        ## The provider wasn't able to successfully authenticate the principal.
        AUTHENTICATION_FAILED = "{}AuthnFailed".format(_PREFIX)

        ## Unexpected or invalid content was encountered.
        INVALID_ATTRIBUTE_NAME_OR_VALUE = "{}InvalidAttrNameOrValue".format(
            _PREFIX)

        ## The responding provider cannot support the requested name ID policy.
        INVALID_NAME_ID_POLICY = "{}InvalidNameIDPolicy".format(_PREFIX)

        ## The authentication context requirements cannot be met.
        NO_AUTHENTICATION_CONTEXT = "{}NoAuthnContext".format(_PREFIX)

        ## None of the supported identity providers are available.
        NO_AVAILABLE_IDP = "{}NoAvailableIDP".format(_PREFIX)

        ## The responding provider cannot authenticate the principal passively.
        NO_PASSIVE = "{}NoPassive".format(_PREFIX)

        ## None of the identity providers are supported by the intermediary.
        NO_SUPPORTED_IDP = "{}NoSupportedIDP".format(_PREFIX)

        ## Not able to propagate logout to all other session participants.
        PARTIAL_LOGOUT = "{}PartialLogout".format(_PREFIX)

        ## Cannot authenticate directly and not permitted to proxy the request.
        PROXY_COUNT_EXCEEDED = "{}ProxyCountExceeded".format(_PREFIX)

        ## Is able to process the request but has chosen not to respond.
        REQUEST_DENIED = "{}RequestDenied".format(_PREFIX)

        ## The SAML responder or SAML authority does not support the request.
        REQUEST_UNSUPPORTED = "{}RequestUnsupported".format(_PREFIX)

        ## Deprecated protocol version specified in the request.
        REQUEST_VERSION_DEPRECATED = "{}RequestVersionDeprecated".format(
            _PREFIX)

        ## Protocol version specified in the request message is too low.
        REQUEST_VERSION_TOO_LOW = "{}RequestVersionTooHigh".format(_PREFIX)

        ## Protocol version specified in the request message is too high.
        REQUEST_VERSION_TOO_HIGH = "{}RequestVersionTooLow".format(_PREFIX)

        ## Resource value provided in the request message is invalid.
        RESOURCE_NOT_RECOGNIZED = "{}ResourceNotRecognized".format(_PREFIX)

        ## The response message would contain more elements than able.
        TOO_MANY_RESPONSES = "{}TooManyResponses".format(_PREFIX)

        ## Attribute from an unknown attribute profile.
        UNKNOWN_ATTR_PROFILE = "{}UnknownAttrProfile".format(_PREFIX)

        ## The responder does not recognize the principal.
        UNKNOWN_PRINCIPAL = "{}UnknownPrincipal".format(_PREFIX)

        ## The SAML responder cannot properly fulfill the request.
        UNSUPPORTED_BINDING = "{}UnsupportedBinding".format(_PREFIX)

    ## The status code value.
    value = attribute.Attribute("Value", required=True)

    ## \todo Element <StatusCode>


class Status(Element):
    """Represents a status returned with the response.
    """

    ## A code representing the status of the activity carried out.
    code = StatusCode(meta__min_occurs=1)

    ## A message which may be returned to give further clarification.
    message = element.Simple(
        name="StatusMessage",
        namespace=Element.Meta.namespace)

    # \todo Element <StatusDetail>


class StatusResponseType(Message):
    """
    Defines commonalities among all SAML protocol messages that return a
    status code along with the response.
    """

    ## A reference to the identifier of the initiating request.
    in_response_to = attribute.Attribute("InResponseTo")

    ## A code representing the status of the corresponding request.
    status = Status()


## \todo Element <AssertionIDRequest>
## \todo Element <SubjectQuery>
## \todo Element <AuthnQuery>
## \todo Element <RequestedAuthnContext>
## \todo Element <AttributeQuery>
## \todo Element <AuthzDecisionQuery>


class Response(StatusResponseType):
    """Used when a response consists of a list of zero or more assertions.
    """

    ## Specifies an (optionally encrypted) assertion by value.
    assertion = saml.Assertion(meta__max_occurs=None)


class AuthenticationRequest(Message):
    """To request authentication with an identity provider.
    """

    class Meta(Message.Meta):
        name = 'AuthnRequest'

    ## Specifies the requested subject of the resulting assertion(s).
    subject = saml.Subject()

    ## \todo Element <NameIDPolicy>
    ## \todo Element <saml:Conditions>
    ## \todo Element <RequestedAuthnContext>
    ## \todo Element <Scoping>

    ## If true, the identity provider MUST authenticate.
    is_forced = attribute.BooleanAttribute("ForceAuthn")

    ## If true, the identity provider itself MUST NOT visibly take control.
    is_passive = attribute.BooleanAttribute("IsPassive")

    ## Indirectly identifies the location of where to send the response.
    assertion_consumer_service_index = attribute.Attribute(
        "AssertionConsumerServiceIndex")

    ## Specifies the location to which the <Response> message must be sent.
    assertion_consumer_service_url = attribute.Attribute(
        "AssertionConsumerServiceURL")

    ## A URI reference that identifies a SAML protocol binding to be used.
    protocol_binding = attribute.Attribute(
        name="ProtocolBinding",
        required=True,
        default=Element.Meta.namespace[1])

    ## Indirectly identifies the SAML attributes the requester desires.
    attribute_consuming_service_index = attribute.Attribute(
        "AttributeConsumingServiceIndex")

    ## Specifies the human-readable name of the requester.
    provider_name = attribute.Attribute("ProviderName")


## \todo Element <NameIDPolicy>
## \todo Element <Scoping>
## \todo Element <IDPList>
## \todo Element <IDPEntry>


class ArtifactResolve(Message):
    """
    Used to request that a SAML protocol message be returned in exchange
    for a previously sent artifact.
    """

    ## Artifact value that the requester received and wishes to resolve.
    artifact = element.Simple(
        name='Artifact',
        namespace=Message.Meta.namespace)


class ArtifactResponse(StatusResponseType):
    """Contains a SAML message being returned from an ArtifactResolve message.
    """

    ## The SAML protocol message being returned.
    message = element.Element(meta__min_occurs=1)


## \todo Element <ManageNameIDRequest>
## \todo Element <ManageNameIDResponse>


class LogoutRequest(Message):
    """
    A message a session participant or session authority to indicate that a
    session has been terminated.
    """

    ## The time at which the request expires.
    not_on_or_after = attribute.DateTimeAttribute('NotOnOrAfter')

    ## An indication of the reason for the logout, as a URI reference.
    reason = attribute.Attribute('Reason')

    ## The principal to terminate the session of.
    principal = saml.BaseIDAbstractType()

    ## The identifier that indexes this session at the message recipient.
    session = element.Simple(
        name='SessionIndex',
        index=1,
        namespace=Message.Meta.namespace)


class LogoutResponse(StatusResponseType):
    """A response to indicate the success of a logout request."""
    pass


## \todo Element <NameIDMappingRequest>
## \todo Element <NameIDMappingResponse>
