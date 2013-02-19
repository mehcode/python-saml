# -*- coding: utf-8 -*-
"""Defines the XML data types for SAML2 in the md namespace.
"""
from uuid import uuid4
from datetime import datetime
from .. import VERSION
from . import attribute, element


class Element(element.Element):
    class Meta(element.Element.Meta):
        namespace = ("md", "urn:oasis:names:tc:SAML:2.0:metadata")

# """Element classes are being arranged in alphabetical order"""

class AffiliationDescriptor(Element):
    affliation_owner_id = attribute.Attribute(
        name="affiliationOwnerID",
        required=True)
    id = attribute.Attribute(
        name="ID",
        default=lambda: '_{}'.format(uuid4(), hex))
    valid_until = attribute.Attribute("validUntil")
    cache_duration = attribute.Attribute("cacheDuration")


class AttributeConsumingService(Element):
    index = attribute.Attribute(
        name="index",
        required=True)
    is_default = attribute.Attribute("isDefault")



class EndPointType(Element):
    binding = attribute.Attribute(
        name="Binding",
        required=True)

    location = attribute.Attribute(
        name="Location",
        required=True)

    response_location = attribute.Attribute(
        name="ResponseLocation")


class EntitiesOrEntityDescriptor(Element):
    pass


class EntitiesDescriptor(EntitiesOrEntityDescriptor):
    id = attribute.Attribute(
        name="ID",
        default=lambda: '_{}'.format(uuid4(), hex))

    valid_until = attribute.DateTimeAttribute("ValidUntil")

    cache_duration = attribute.Attribute("CacheDuration")

    ## In the standard blah
    name = attribute.Attribute("Name")

## \todo: implement signatures

    descriptors = EntitiesOrEntityDescriptor(
        meta__min_occurs=1, meta__max_occurs=None)


class RoleDescriptor(Element):
    id = attribute.Attribute(
        name="id",
        default=lambda: '_{}'.format(uuid4(), hex))

    valid_until = attribute.DateTimeAttribute("validUntil")

    cache_duration = attribute.Attribute("cacheDuration")

    protocols_support_enumeration = attribute.Attribute(
        name="protocolsSupportEnumeration",
        required=True)

    error_url = attribute.Attribute("errorURL")


class EntityDescriptor(EntitiesOrEntityDescriptor):
    entityID = attribute.Attribute(
        name="entityID",
        required=True)

    id = attribute.Attribute(
        name="ID",
        default=lambda: '_{}'.format(uuid4(), hex))

    valid_until = attribute.DateTimeAttribute("ValidUntil")

    cache_duration = attribute.Attribute("CacheDuration")

    name = attribute.Attribute("Name")

    descriptors = RoleDescriptor(meta__min_occurs=1, meta__max_occurs=None)


class IndexedEndpointType(EndPointType):
    index = attribute.Attribute(
        name="index",
        required=True)

    is_default = attribute.Attribute("isDefault")


class Organization(Element):
    extension = element.Element(name = "Extensions")
    organization_name = element.Element(name = "OrganizationName", meta__min_occurs = 1, meta__max_occurs = None)
    organization_display_name = element.Element(name = "OrganizationDisplayName", meta__min_occurs = 1, meta__max_occurs = None)
    organization_url = element.Element(name = "OrganizationURL", meta__min_occurs = 1, meta__max_occurs = None)

class RequestedAttribute(Element):
    is_required = attribute.Attribute("isRequred")
