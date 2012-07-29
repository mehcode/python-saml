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
