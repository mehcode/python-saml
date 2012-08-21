# -*- coding: utf-8 -*-
""" \file saml/schema/attribute.py
\brief Defines base attribute classes for the schema package.

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
