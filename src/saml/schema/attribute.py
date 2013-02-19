# -*- coding: utf-8 -*-
"""Defines base attribute classes for the schema package.
"""
from datetime import datetime


class Attribute(object):
    """Represents a generic attribute on an XML element."""

    @staticmethod
    def deserialize(value):
        """Returns the passed value."""
        return value

    @staticmethod
    def serialize(value):
        """Stringifys the passed value."""
        return str(value)

    def __init__(self, name, default=None, required=False):
        """Initialize an attribute with constraints on its values."""
        ## Name of the attribute.
        self.name = name

        ## A default value that can be used.
        self.default = default

        ## Whether to raise an exception upon serialization if not provided.
        self.required = required


class BooleanAttribute(Attribute):
    """Represents a boolean attribute on an XML element."""

    @staticmethod
    def deserialize(value):
        """Returns a boolean from the passedhttps xs:bool XML value."""
        return True if value.lower() == "true" else False

    @staticmethod
    def serialize(value):
        """Stringifys the passed value."""
        return "true" if value else "false"


class DateTimeAttribute(Attribute):
    """Represents a date/time attribute on an XML element."""

    @staticmethod
    def deserialize(value):
        """Returns a datetime from the passed xs:dateTime XML value."""
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')

    @staticmethod
    def serialize(value):
        """Stringifys the passed value."""
        return value.strftime('%Y-%m-%dT%H:%M:%SZ')
