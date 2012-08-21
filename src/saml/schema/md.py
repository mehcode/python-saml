# -*- coding: utf-8 -*-
""" \file saml/schema/md.py
\brief Defines the XML data types for SAML2 in the md namespace.

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
        namespace = ("md", "urn:oasis:names:tc:SAML:2.0:metadata")

# """Element classes are being arranged in alphabetical order"""

class AttributeConsumingService(Element):
    index = attribute.Attribute(
        name = "index",
        required = True)
    is_default = attribute.Attribute("isDefault")
    


class EndPointType(Element):
    binding = attribute.Attribute(
        name = "Binding",
        required = True)

    location = attribute.Attribute(
        name = "Location",
        required = True)

    response_location = attribute.Attribute(
        name = "ResponseLocation")


class EntitiesDescriptor(Element):
    id = attribute.Attribute(
        name = "ID",
        default = lambda: '_{}'.format(uuid4(), hex))

    valid_until = attribute.DateTimeAttribute("ValidUntil")

    cache_duration = attribute.Attribute("CacheDuration")

    ## In the standard blah
    name = attribute.Attribute("Name")


class RoleDescriptor(Element):
    id = attribute.Attribute(
        name = "id",
        default = lambda: '_{}'.format(uuid4(), hex))

    valid_until = attribute.DateTimeAttribute("validUntil")

    cache_duration = attribute.Attribute("cacheDuration")

    protocols_support_enumeration = attribute.Attribute(
        name = "protocolsSupportEnumeration",
        required = True)

    error_url = attribute.Attribute("errorURL")


class EntityDescriptor(Element):
    entity_id = attribute.Attribute(
        name = "entityID",
        required = True)

    id = attribute.Attribute(
        name = "ID",
        default = lambda: '_{}'.format(uuid4(), hex))

    valid_until = attribute.DateTimeAttribute("ValidUntil")

    cache_duration = attribute.Attribute("CacheDuration")

    name = attribute.Attribute("Name")

    descriptors = RoleDescriptor(meta__min_occurs=1, meta__max_occurs=None)


class IndexedEndpointType(EndPointType):
    index = attribute.Attribute(
        name="index",
        required=True)

    is_default = attribute.Attribute("isDefault")
