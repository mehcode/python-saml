# -*- coding: utf-8 -*-
""" \file saml/schema/element.py
\brief Defines base element classes for the schema package.

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
import inspect
from lxml.builder import ElementMaker
from lxml import etree
from . import attribute


class Element(object):
    """Represents a generic element on an XML element.
    """

    class Meta:
        """Base meta object if none is provided in derived object.
        """
        pass

    @staticmethod
    def deserialize(text):
        """Deserialize the passed text as an element.
        """
        pass

    @classmethod
    def _get_ordered_members(cls):
        """"""
        sorted = []

        # Add members from base classes, recursively
        for base in cls.__bases__:
            try:
                sorted.extend(base._get_ordered_members())
            except AttributeError:
                # Reached object, we're done
                pass

        # Add members from calling class
        for name, value in cls.__dict__.items():
            if isinstance(value, Element):
                if hasattr(value, '_meta') and hasattr(value._meta, 'index'):
                    sorted.append((value._meta.index, name, value))
                else:
                    sorted.append((0, name, value))
            if isinstance(value, Simple):
                sorted.append((value.index, name, value))
            elif isinstance(value, attribute.Attribute):
                sorted.append((0, name, value))

        return sorted

    @classmethod
    def serialize(cls, obj):
        """Serializes the passed element into an XML representation."""
        # Instantiate an element maker context
        E = ElementMaker(
            namespace=obj._meta.namespace[1],
            nsmap={obj._meta.namespace[0]: obj._meta.namespace[1]}
        )

        # Instantiate an XML element with its name
        xml = E(obj._meta.name)

        # Append text content (if available)
        if hasattr(obj, "text"):
            xml.text = str(obj.text)

        # Iterate through ordered list of members to serialize and append
        for unused, name, value in cls._get_ordered_members():
            # Was this member provided ?
            attr = obj.__dict__.get(name)
            if attr is not None and value is not None:
                if isinstance(value, attribute.Attribute):
                    # Set as an attribute if it is derived from
                    # the base Attribute class.
                    xml.set(value.name, value.serialize(attr))
                elif isinstance(value, Element):
                    # Serialize and append as an element if it is derived
                    # from the base Element class
                    try:
                        # First; try appending several as an iterable
                        for item in attr:
                            xml.append(value.serialize(item))
                    except TypeError:
                        # Didn't work; this must be a singular element
                        xml.append(value.serialize(attr))

        # Return serialized XML
        return xml

#    def serialize(self):
#        """Serialize the current element as text.
#        """
#        # Instantiate an element maker tailored for this element
#        E = ElementMaker(
#            namespace=self._meta.namespace[1],
#            nsmap={self._meta.namespace[0]: self._meta.namespace[1]})
#
#        # Instantiate an XML element with its name
#        xml = E(self._meta.name)
#
#        # Append text, if available
#        if hasattr(self, "text"):
#            xml.text = str(self.text)
#
#        # Append elements
#        for index, name, value in self._get_ordered_members():
#            # Does this exist ?
#            attr = self.__dict__.get(name)
#            if attr is not None and value is not None:
#                # Attempt to set this as an attribute
#                try:
#                    xml.set(value.name, value.serialize(attr))
#                    continue
#                except:
#                    pass
#
#                # Attempt to set this as a simple element
#                try:
#                    xml.append(etree.XML(value.serialize(attr)))
#                    continue
#                except:
#                    pass
#
#                # Loop through and append all elements as XML
#                try:
#                    for item in attr:
#                        # FIXME: This etree.XML(..) is stupid
#                        xml.append(etree.XML(item.serialize()))
#                    continue
#                except:
#                    pass
#
#                # Or can this be directly serialized as XML ?
#                try:
#                    # FIXME: This etree.XML(..) is stupid
#                    xml.append(etree.XML(attr.serialize()))
#                    continue
#                except:
#                    # We have no idea what this... just fail silently
#                    pass
#
#        # Return the XML element as string
#        return etree.tostring(xml)

    def __init__(self, text=None, **kwargs):
        """Instantiates an element reference.
        """
        ## Metadata about the element
        self._meta = self.__class__.Meta()

        # Declare any defaults, if present
        for name, value in inspect.getmembers(self.__class__):
            # If there was a default provided
            if hasattr(value, 'default') and value.default is not None:
                # Then supply it
                try:
                    # Either it is a callable that will generate a
                    # default
                    self.__dict__[name] = value.default()
                except:
                    # Or simply a scalar
                    self.__dict__[name] = value.default

        # Default value for meta elements
        self._meta.__dict__.update(inspect.getmembers(self._meta.__class__))
        self._meta.name = self.__class__.__name__

        # Iterate through and update object dictionaries from passed values
        for name, value in kwargs.items():
            segs = name.split("__")
            if segs[0] == 'meta':
                # Was passed as meta__X so set X of meta to value
                self._meta.__dict__[segs[1]] = value
            else:
                # Was passed normally, so set normally
                self.__dict__[name] = value

        # Did we receive any text ?
        if text is not None:
            self.text = text


class Simple(object):
    """
    Represents a 'simple' element that acts like an attribute of the object but
    is serialized and deserialized as an XML element.
    """
    def __init__(self, name, index=None, namespace=None, default=None):
        """Initialize a simple element with constraints on its values."""
        ## Name of the simple.
        self.name = name

        ## Namespace of the simple.
        self.namespace = namespace

        ## Index of the simple.
        self.index = index if index is not None else 0

        ## A default value that can be used.
        self.default = default

#    def serialize(self, obj):
#        """Serialize the current element as text.
#        """
#        # Instantiate an element maker tailored for this element
#        E = ElementMaker(
#            namespace=self.namespace[1],
#            nsmap={self.namespace[0]: self.namespace[1]})
#
#        # Instantiate an XML element with its name
#        xml = E(self.name)
#
#        # Append content
#        xml.text = str(obj)
#
#        # Return constructed XML block
#        return etree.tostring(xml)
