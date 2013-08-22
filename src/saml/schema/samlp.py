from uuid import uuid4
from datetime import datetime
from . import types, base, VERSION, Attribute, Element, saml


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
    protocol_binding = Attribute(types.String)

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
