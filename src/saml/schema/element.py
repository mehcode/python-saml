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


class Element(object):
    """Represents a generic element on an XML element.
    """

    class Meta:
        """Base meta object if none is provided in derived object.
        """
        pass

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
    def __init__(self, name, default=None):
        """Initialize a simple element with constraints on its values."""
        ## Name of the attribute.
        self.name = name

        ## A default value that can be used.
        self.default = default
