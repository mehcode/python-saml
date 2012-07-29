# -*- coding: utf-8 -*-
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
import operator
from lxml.builder import ElementMaker
from datetime import datetime
from collections import OrderedDict


class Attribute(object):
    """Represents an attribute on an XML element."""

    @staticmethod
    def fromstring(value):
        """TODO"""
        return value

    @staticmethod
    def tostring(value):
        """TODO"""
        return str(value)

    def __init__(
            self,
            index,
            name,
            default=None,
            required=False):
        """TODO"""
        ## Index of the type in the contained element.
        ## NOTE: This is used to preserve declared order in a class; this can
        ## be removed come python3.
        self.index = index

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
        """TODO"""
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')

    @staticmethod
    def tostring(value):
        """TODO"""
        return value.strftime('%Y-%m-%dT%H:%M:%SZ')


class Element(object):
    """TODO
    """

    @classmethod
    def fromxml(cls, xml):
        """TODO"""
        pass

    def __init__(
            self,
            index,
            cls,
            default=None,
            min_occurs=0,
            max_occurs=1):
        """TODO"""
        ## Index of the type in the contained element.
        ## NOTE: This is used to preserve declared order in a class; this can
        ## be removed come python3.
        self.index = index

        ## Class object of the type (also represents the name).
        self.cls = cls

        ## A default value that can be used if none is defined by the
        ## user.
        self.default = default

        ## Number of elements that must be provided at a minimum.
        self.min_occurs = min_occurs

        ## Number of elements that must be provided at a maximum.
        self.max_occurs = max_occurs

    def toxml(self, obj):
        """
        Generates an XML representation of this element from its defined
        attributes and content.
        """
        # Instantiate an element maker tailored for this element
        E = ElementMaker(
            namespace=obj.namespace[1],
            nsmap={obj.namespace[0]: obj.namespace[1]})

        # Instantiate the XML element maker with its name
        xml = E(obj.__class__.__name__)

        # Append content if available
        if hasattr(obj, "value"):
            xml.text = str(obj.value)

        # Construct sorted list of items
        sort = {}
        for name, attr in obj.__class__.__dict__.items():
            if hasattr(attr, 'index') and not name.startswith('__'):
                sort.update({name: attr.index})

        sort = sorted(sort.iteritems(), key=operator.itemgetter(1))
        sort = [(x[0], obj.__dict__.get(x[0], None)) for x in sort]

        # Append available attributes and elements
        for name, value in sort:
            # Does this exist ?
            attr = getattr(obj.__class__, name, None)
            if attr is not None and value is not None:
                # Attempt to set this as an attribute
                try:
                    xml.set(attr.name, attr.tostring(value))
                    continue
                except:
                    pass

                # Is this a raw string ?
                if isinstance(value, basestring):
                    xml.append(attr.toxml(value))
                    continue

                # Loop through and append all elements as XML
                # as we assume (and require) iterables to iterate over
                # an object that has a toxml() function.
                try:
                    for item in value:
                        xml.append(attr.toxml(item))
                    continue
                except:
                    # We have no idea what this... just fail silently
                    pass

                # Or can this be directly serialized as XML ?
                try:
                    xml.append(attr.toxml(value))
                    continue
                except BaseException as x:
                    pass

        # Return constructed XML block
        return xml


class SimpleElement(Element):
    """TODO
    """

    @classmethod
    def fromxml(cls, xml):
        """TODO"""
        pass

    def __init__(self, index, name, namespace, default=None):
        """TODO"""
        ## Index of the type in the contained element.
        ## NOTE: This is used to preserve declared order in a class; this can
        ## be removed come python3.
        self.index = index

        ## Name of the element.
        self.name = name

        ## Namespace of the element.
        self.namespace = namespace

        ## A default value that can be used if none is defined by the
        ## user.
        self.default = default

    def toxml(self, obj):
        """
        Generates an XML representation of this element from its defined
        attributes and content.
        """
        # Instantiate an element maker tailored for this element
        E = ElementMaker(
            namespace=self.namespace[1],
            nsmap={self.namespace[0]: self.namespace[1]})

        # Instantiate the XML element maker with its name
        xml = E(self.name)

        # Append content if available
        xml.text = str(obj)

        # Return constructed XML block
        return xml


class Type(object):
    """TODO
    """

    def __init__(self, value=None, **kwargs):
        """TODO"""
        # Update value if provided
        if value is not None:
            self.value = value

        # Declare defaults
        for name, value in self.__class__.__dict__.items():
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

        # Update internal dictionary with provided values
        self.__dict__.update(**kwargs)
