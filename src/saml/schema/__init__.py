""" \file saml/schema/__init__.py
\brief Defines helper classes for the schema package.

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
from lxml.builder import ElementMaker
from datetime import datetime
import dateutil


class Attribute(object):
    """Represents an attribute on an XML element."""

    @staticmethod
    def fromstring(value):
        return value

    @staticmethod
    def tostring(value):
        return str(value)

    def __init__(
            self,
            name,
            default=None,
            required=False):
        ## Name of the attribute.
        self.name = name

        ## A default value that can be used if none is defined by the
        ## user.
        self.default = default

        ## Whether to raise an exception upon producing as XML
        ## if this attribute was not provided.
        self.required = required


class DateTimeAttribute(Attribute):
    """Represents a date time attribute on an XML element."""

    @staticmethod
    def fromstring(value):
        return dateutil.parse(value)

    @staticmethod
    def tostring(value):
        return value.isoformat()

class Type(object):
    def __init__(self, value=None, **kwargs):
        # Update value if provided
        if value is not None:
            self.value = value

        # Declare defaults
        for name, value in self.__class__.__dict__.items():
            # Currently we only support defaults on attributes
            if isinstance(value, Attribute):
                # If there was a default provided
                if value.default is not None:
                    # Then supply it
                    try:
                        # Either it is a callable that will generate a
                        # default
                        self.__dict__[name] = value.default()
                    except:
                        # Or simply a scalar
                        self.__dict__[name] = value.default

        # Update internal dictionary with provided values
        self.__dict__.update(**kwargs)


class Element(object):
    @classmethod
    def fromxml(cls, xml):
        pass

    def toxml(self):
        """
        Generates an XML representation of this element from its defined
        attributes and content.
        """
        # Instantiate an element maker tailored for this element
        E = ElementMaker(
            namespace=self.namespace[1],
            nsmap={self.namespace[0]: self.namespace[1]})

        # Instantiate the XML element with its name
        xml = E(self.__class__.__name__)

        # Append content if available
        if hasattr(self, "value"):
            xml.text = str(self.value)

        # Append available attributes and elements
        for name, value in self.__dict__.items():
            # Does this exist ?
            attr = getattr(self.__class__, name, None)
            if attr is not None:
                # Does this exist as an attribute ?
                if isinstance(attr, Attribute):
                    # Yes; set the attribute value
                    xml.set(attr.name, attr.tostring(value))
                # Or can this be serialized as XML ?
                elif hasattr(value, "toxml"):
                    # Append it as an XML element
                    xml.append(value.toxml())
                # Or is this some kind of iterable ?
                else:
                    # Loop through and append all elements as XML
                    # as we assume (and require) iterables to iterate over
                    # an object that has a toxml() function.
                    try:
                        for item in value:
                            xml.append(item.toxml())
                    except:
                        # We have no idea what this... just fail silently
                        pass

        # Return constructed XML block
        return xml
