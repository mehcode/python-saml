# -*- coding: utf-8 -*-
"""Defines base element classes for the schema package.
"""
import inspect
from lxml.builder import ElementMaker
from . import attribute


class Element(object):
    """Represents a generic element on an XML element.
    """

    class Meta:
        """Base meta object if none is provided in derived object.
        """
        pass

    @classmethod
    def _get_ordered_members(cls):
        """"""
        ordered = []

        # Add members from base classes, recursively
        for base in cls.__bases__:
            try:
                ordered.extend(base._get_ordered_members())
            except AttributeError:
                # Reached object, we're done
                pass

        # Collect members of current cls into one list
        sub = []

        # Add members from calling class
        for name, value in cls.__dict__.items():
            if isinstance(value, Element):
                if hasattr(value, '_meta') and hasattr(value._meta, 'index'):
                    sub.append((value._meta.index, name, value))
                else:
                    sub.append((0, name, value))
            if isinstance(value, Simple):
                sub.append((value.index, name, value))
            elif isinstance(value, attribute.Attribute):
                sub.append((0, name, value))

        # Sort current class members before adding to main ordered list
        ordered.extend(sorted(sub))

        # Return list
        return ordered

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
                            xml.append(item.serialize(item))
                    except TypeError:
                        # Didn't work; just serialize it
                        xml.append(attr.serialize(attr))
                elif isinstance(value, Simple):
                    # Serialize and append the simple element
                    xml.append(value.serialize(value, attr))

        # Return serialized XML
        return xml

    @classmethod
    def deserialize(cls, xml):
        """Deserialize the passed XML as an element."""
        # Import neccessary files
        from . import samlp, saml, md

        # The name cache is used to find the class from from its meta name
        # It is basically a dictionary in which the keys are the Meta.name
        # and the values are the class objects. It makes deserialization
        # actually possible in a speedy manner

        # Is name cache available ?
        if not hasattr(Element, '_name_cache'):
            # Nope; create name cache
            Element._name_cache = {}

            # Iterate through list of classes
            for module in (samlp, saml, md):
                for klass in module.__dict__.values():
                    try:
                        if issubclass(klass, Element):
                            meta = klass()._meta
                            key = '{}.{}'.format(meta.namespace[0], meta.name)
                            Element._name_cache[key] = klass
                    except:
                        pass

        # Instantiate class
        obj = cls()

        # Get list
        elements = xml.getchildren()
        index = 0

        # Iterate through ordered members
        for unused, name, member in cls._get_ordered_members():
            store_index = index
            try:
                if isinstance(member, Element):
                    # Iterate N times; the -1 keeps the iteration
                    # until failure
                    iteration = 0
                    maximum = member._meta.max_occurs or -1
                    while iteration != maximum:
                        # Get element in question
                        element = elements[index]

                        # Invert nsmap dictionary
                        nsmap = {x: y for y, x in element.nsmap.items()}

                        # Get tag name and namespace
                        tag = element.tag.split('{')[1].split('}')

                        # Build name
                        cachedname = '{}.{}'.format(nsmap[tag[0]], tag[1])

                        # Get klass from cache
                        klass = Element._name_cache[cachedname]

                        # Fail safe; someone gave us garbage
                        if not issubclass(klass, member.__class__):
                            raise Exception()

                        # Deserialize using klass
                        kobj = klass.deserialize(element)

                        # Does this already exist in the obj
                        if name in obj.__dict__:
                            try:
                                # Attempt to just append it
                                obj.__dict__[name].append(kobj)
                            except AttributeError:
                                # Nope; make it a list first
                                obj.__dict__[name] = [obj.__dict__[name], kobj]
                        else:
                            # Nope; put it there
                            obj.__dict__[name] = kobj

                        # Increment counter
                        iteration += 1
                        index += 1
                elif isinstance(member, Simple):
                    # Get element in question
                    element = elements[index]

                    # Deserialize and store in the dict
                    obj.__dict__[name] = member.deserialize(member, element)

                    # Increment
                    index += 1
                elif isinstance(member, attribute.Attribute):
                    # Does this exist in the XML ?
                    value = xml.get(member.name)
                    if value is not None:
                        # Yes; deserialize and set it
                        obj.__dict__[name] = member.deserialize(value)
            except IndexError:
                # Ran out of XML elements; might as well stop
                break
            except:
                # Something went wrong; reset the iterator
                index = store_index

        # Get simple content
        if xml.text and xml.text.strip():
            obj.text = xml.text.strip()

        # Return instance
        return obj

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
        self._meta.name = self.__class__.__name__
        self._meta.min_occurs = 0
        self._meta.max_occurs = 1
        self._meta.__dict__.update(inspect.getmembers(self._meta.__class__))

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

    @staticmethod
    def deserialize(obj, xml):
        """Deserializes the passed xml value."""
        # Screw complicated; just return the value
        return xml.text

    @classmethod
    def serialize(cls, obj, value):
        """Serializes the passed element as a 'simple' element."""
        # Instantiate an element maker context
        E = ElementMaker(
            namespace=obj.namespace[1],
            nsmap={obj.namespace[0]: obj.namespace[1]}
        )

        # Instantiate an XML element with its name
        xml = E(obj.name)

        # Append "simple" content
        xml.text = str(value)

        # Return constructed element
        return xml

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
