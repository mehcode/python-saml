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


class Type(object):
    def __init__(self, value=None, **kwargs):
        # Update value if provided
        if value is not None:
            self.value = value

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
        if hasattr(self, 'value'):
            xml.text = str(self.value)

        # Append available attributes and children
        for name, value in self.__dict__.items():
            # Does this exist ?
            attr = getattr(self.__class__, name, None)
            if attr is not None:
                # Does this exist as an attribute ?
                if isinstance(attr, Attribute):
                    # Yes; set the attribute value
                    xml.set(attr.name, value)

        # Return constructed XML block
        return xml


class Attribute(object):
    """Represents an attribute on an XML element."""
    def __init__(self, name):
        ## Name of the attribute.
        self.name = name
