# -*- coding: utf-8 -*-
""" \file saml/schema/samlp.py
\brief Defines the XML data types for SAML2 in the samlp namespace.

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
from .. import VERSION
from .. import schema
from uuid import uuid4
from datetime import datetime
from . import saml


class Type(schema.Type):
    """Represents a type in this namespace."""
    namespace = ("samlp", "urn:oasis:names:tc:SAML:2.0:protocol")


class Message(Type):
    """
    Defines common attributes and elements that are associated with
    all SAML messages.
    """

    ## The identifier for this message.
    id = schema.Attribute(
        index=0,
        name="ID",
        required=True,
        default=lambda: '_{}'.format(uuid4().hex))

    ## The version of this message.
    version = schema.Attribute(1, "Version", required=True, default=VERSION)

    ## The time instant of issue in UTC.
    issue_instant = schema.DateTimeAttribute(
        index=2,
        name="IssueInstant",
        required=True,
        default=datetime.utcnow)

    ## A URI reference indicating the address to which this message has
    ## been sent.
    destination = schema.Attribute(3, "Destination")

    ## Identifies the entity that generated the message.
    issuer = schema.Element(4, saml.Issuer, min_occurs=1)

    ## Indicates whether or not (and under what conditions) consent has been
    ## obtained from a principal in the sending of this message.
    consent = schema.Attribute(5, "Consent")

    ## \todo Element <ds:Signature>
    ## \todo Element <Extensions>


class RequestAbstractType(Message):
    """
    Defines common attributes and elements that are associated with
    all SAML requests.
    """


## \todo Element <Status>
## \todo Element <StatusCode>
## \todo Element <StatusMessage>
## \todo Element <StatusDetail>


class StatusResponseType(Message):
    """
    Defines common attributes and elements that are associated with all
    SAML responses.
    """

    ## A reference to the identifier of the request to which the response
    ## corresponds, if any.
    in_response_to = schema.Attribute(6, "InResponseTo")

## \todo Element <AssertionIDRequest>
## \todo Element <SubjectQuery>
## \todo Element <AuthnQuery>
## \todo Element <RequestedAuthnContext>
## \todo Element <AttributeQuery>
## \todo Element <AuthzDecisionQuery>

## \todo Element <Response>

## \todo Element <AuthnRequest>


class AuthnRequest(RequestAbstractType):
    """
    To request that an identity provider issue an assertion with an
    authentication statement, a presenter authenticates to that
    identity provider (or relies on an existing security context) and sends
    it an <AuthnRequest> message that describes the properties that the
    resulting assertion needs to have to satisfy its purpose.
    """
    ## Specifies the requested subject of the resulting assertion(s).
    subject = schema.Element(6, saml.Subject)

    ## Specifies constraints on the name identifier to be used to represent
    ## the requested subject.
    #name_id_policy = schema.Element(7, NameIDPolicy)

    ## \todo Element <saml:Conditions>

    ## Specifies the requirements, if any, that the requester places on the
    ## authentication context that applies to the responding provider's
    ## authentication of the presenter.
    #requested_authn_context = schema.Element(8, RequestedAuthnContext)

    ## Specifies a set of identity providers trusted by the requester to
    ## authenticate the presenter, as well as limitations and context related
    ## to proxying of the <AuthnRequest> message to subsequent identity
    ## providers by the responder.
    #scoping = schema.Element(9, Scoping)

    ## A Boolean value. If "true", the identity provider MUST authenticate
    ## the presenter directly rather than rely on a previous security
    ## context. If a value is not provided, the default is "false".
    force_authn = schema.Attribute(10, "ForceAuthn")

    ## A Boolean value. If "true", the identity provider and the user agent
    ## itself MUST NOT visibly take control of the user interface from the
    ## requester and interact with the presenter in a noticeable fashion.
    is_passive = schema.Attribute(11, "IsPassive")

    ## Indirectly identifies the location to which the <Response> message
    ## should be returned to the requester.
    assertion_consumer_service_index = schema.Attribute(
        index=12,
        name="AssertionConsumerServiceIndex")

    ## Specifies by value the location to which the <Response> message
    ## MUST be returned to the requester
    assertion_consumer_service_url = schema.Attribute(
        index=13,
        name="AssertionConsumerServiceURL")

    ## A URI reference that identifies a SAML protocol binding to be used
    ## when returning the <Response> message.
    protocol_binding = schema.Attribute(
        index=14,
        name="ProtocolBinding",
        default=Type.namespace[1])

    ## Indirectly identifies information associated with the requester
    ## describing the SAML attributes the requester desires or requires to be
    ## supplied by the identity provider in the <Response> message.
    attribute_consuming_service_index = schema.Attribute(
        index=15,
        name="AttributeConsumingServiceIndex")

    ## Specifies the human-readable name of the requester for use by the
    ## presenter's user agent or the identity provider.
    provider_name = schema.Attribute(16, "ProviderName")

## \todo Element <NameIDPolicy>
## \todo Element <Scoping>
## \todo Element <IDPList>
## \todo Element <IDPEntry>
## \todo Element <ArtifactResolve>
## \todo Element <ArtifactResponse>
## \todo Element <ManageNameIDRequest>
## \todo Element <ManageNameIDResponse>
## \todo Element <LogoutRequest>
## \todo Element <LogoutResponse>
## \todo Element <NameIDMappingRequest>
## \todo Element <NameIDMappingResponse>
