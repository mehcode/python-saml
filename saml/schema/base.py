# -*- coding: utf-8 -*-
from collections import OrderedDict
from lxml import etree
import six
from .utils import pascalize, classproperty


class Options(object):

    def __init__(self, meta, name, data, bases):
        """
        Initializes the options object and defaults configuration not
        specified.
        """

        # Name of the element in its serialized form.
        self.name = meta.get('name')
        if self.name is None:
            # Generate a name if none is provided.
            self.name = pascalize(name)

        # The namespace of the element.
        self.namespace = meta.get('namespace')

        # Index into the elements of where we stick the signature block.
        self.signature_index = meta.get('signature_index', 1)

# Element registry in order to lookup for deserialize.
_element_registry = {}


class Declarative(type):

    @classmethod
    def __prepare__(cls, name, bases):
        return OrderedDict()

    @classmethod
    def _gather_metadata(cls, metadata, bases):
        for base in bases:
            if isinstance(base, cls) and hasattr(base, 'Meta'):
                # Append metadata.
                metadata.append(getattr(base, 'Meta'))

                # Recurse.
                cls._gather_metadata(metadata, base.__bases__)

    @classmethod
    def _is_derived(cls, name, bases):
        for base in bases:
            if isinstance(base, cls):
                # This is some sort of derived resource; good.
                return True

        # This is not derived at all from Resource (eg. is base).
        return False

    def __new__(cls, name, bases, attrs):
        # Only continue if we are dervied from declarative.
        if not cls._is_derived(name, bases):
            return super(Declarative, cls).__new__(
                cls, name, bases, attrs)

        # Gather the attributes of all options classes.
        # Start with the base configuration.
        metadata = {}
        values = lambda x: {n: getattr(x, n) for n in dir(x)}

        # Expand the options class with the gathered metadata.
        base_meta = []
        cls._gather_metadata(base_meta, bases)

        # Apply the configuration from each class in the chain.
        for meta in base_meta:
            metadata.update(**values(meta))

        # Apply the configuration from the current class.
        cur_meta = {}
        if attrs.get('Meta'):
            cur_meta = values(attrs['Meta'])
            metadata.update(**cur_meta)

        # Gather and construct the options object.
        meta = attrs['meta'] = Options(metadata, name, cur_meta, base_meta)

        # Collect declared attributes.
        attrs['_items'] = OrderedDict()

        # Collect attributes from base classes.
        for base in bases:
            values = getattr(base, '_items', None)
            if values:
                attrs['_items'].update(values)

        # Collect attributes from current class.
        test = lambda x: issubclass(type(x[1]), Component)
        attrs_l = list(filter(test, attrs.items()))
        attrs_l.sort(key=lambda x: x[1].creation_counter)
        for key, attr in attrs_l:
            # If name reference is null; default to camel-cased name.
            if attr._name is None:
                attr._name = pascalize(key)

            # Store attribute in dictionary.
            attrs['_items'][attr._name] = attr

        # Continue initialization.
        obj = super(Declarative, cls).__new__(cls, name, bases, attrs)

        # Add this element to the element registry.
        _element_registry[obj.name] = obj

        # Return the constructed element class.
        return obj


class Component(object):

    # Tracks each time this field is created; used to keep fields
    # in order
    creation_counter = 0

    def __init__(self, type_, name=None, required=False, default=None):
        # Name of the attribute in its serialized form.
        self._name = name

        # Underlying type of the attribute.
        self.type = type_

        # Whether the attribute is required or not.
        self.required = required

        # The default value for this attribute.
        self.default = default
        if not callable(default):
            # Normalize self.default to always be a callable.
            self.default = lambda: default

        # Adjust the creation counter, and save our local copy.
        self.creation_counter = Component.creation_counter
        Component.creation_counter += 1

    def __delete__(self, instance):
        if instance is not None:
            # Being accessed as an instance; use the instance state.
            if self._name in instance._state:
                del instance._state[self._name]
                return

        # Prevent deletion.
        raise TypeError("attribute can't be deleted")


class Element(Component):

    def __init__(self, type_, **kwargs):
        # If an element is a collection it is a list of elements.
        self.collection = kwargs.pop('collection', False)

        # Continue the initialization the base element.
        super(Element, self).__init__(type_, **kwargs)

    @property
    def name(self):
        # Return the namespaced name of the element.
        return '{%s}%s' % (self.type.meta.namespace[1], self._name)

    @property
    def namespace(self):
        # Return the namespace of the underlying type.
        return self.type.meta.namespace

    def prepare(self, instance):
        # Retrieve the value of this attribute from the instance.
        value = instance._state.get(self._name)
        if value is None and self.default:
            # No value; use the default callable.
            self.__set__(instance, self.default())
            value = instance._state.get(self._name)

        # Return the value.
        return value

    def deserialize(self, xml):
        return self.type.deserialize(xml)

    def __get__(self, instance, owner=None):
        if instance is not None:
            # Being accessed as an instance; use the instance state.
            value = instance._state.get(self._name)
            if value is None and self.collection:
                # No value and we need to be a collection of things.
                instance._state[self._name] = value = []

            if value is None:
                # Build a default one of ourself.
                instance._state[self._name] = value = self.type()

            # Return the value.
            return value

        # Return ourself.
        return self

    def __set__(self, instance, value):
        if instance is not None:
            if isinstance(value, str):
                # Value is just text; construct the type.
                value = self.type(value)

            # Being accessed as an instance; use the instance state.
            if self.collection:
                if self._name not in instance._state:
                    instance._state[self._name] = []

                instance._state[self._name].append(value)

            else:
                instance._state[self._name] = value

            return

        # Prevent assignment.
        raise TypeError("attribute can't be assigned")


class Attribute(Component):

    def __init__(self, type_, name=None, required=False, default=None):
        # Initialize the base element first.
        super(Attribute, self).__init__(
            type_, name=name, required=required, default=default)

        # Instantiate the type reference with no parameters.
        if isinstance(self.type, type):
            self.type = self.type()

    @property
    def name(self):
        return self._name

    def prepare(self, instance):
        # Retrieve the value of this attribute from the instance.
        value = instance._state.get(self.name)
        if value is None and self.default:
            # No value; use the default callable.
            value = self.default()

        # Run the value through the underyling type's preparation method.
        value = self.type.prepare(value)

        # Return the value.
        return value

    def clean(self, text):
        # Wipe off the passed text and squish it into a python object
        # if needed.
        return self.type.clean(text)

    def __get__(self, instance, owner=None):
        if instance is not None:
            # Being accessed as an instance; use the instance state.
            return instance._state.get(self._name)

        # Return ourself.
        return self

    def __set__(self, instance, value):
        if instance is not None:
            # Being accessed as an instance; use the instance state.
            instance._state[self._name] = value
            return

        # Prevent assignment.
        raise TypeError("attribute can't be assigned")


class Base(six.with_metaclass(Declarative)):

    def __init__(self, text=None, **kwargs):
        # Instance state of the attribute.
        self._state = {}

        # Text of the element.
        self.text = text

        # Update the instance state with kwargs.
        self._state.update(kwargs)

        # The signature function tuple.
        self._sign_args = None

    @classproperty
    def name(cls):
        # Return the namespaced name of the element.
        return '{%s}%s' % (cls.meta.namespace[1], cls.meta.name)

    def prepare(self):
        """Prepare the date in the instance state for serialization.
        """

        # Create a collection for the attributes and elements of
        # this instance.
        attributes, elements = OrderedDict(), []

        # Initialize the namespace map.
        nsmap = dict([self.meta.namespace])

        # Iterate through all declared items.
        for name, item in self._items.items():
            if isinstance(item, Attribute):
                # Prepare the item as an attribute.
                attributes[name] = item.prepare(self)

            elif isinstance(item, Element):
                # Update the nsmap.
                nsmap.update([item.namespace])

                # Prepare the item as an element.
                elements.append(item)

        # Return the collected attributes and elements
        return attributes, elements, nsmap

    def _serialize_item(self, item):
        # Destructure the data.
        attributes, elements, nsmap = item.prepare()

        # Create the XML node.
        node = etree.Element(item.name, nsmap=nsmap)

        # Add the attributes.
        for name, value in attributes.items():
            if value is not None:
                node.attrib[name] = value

        # Set its text.
        node.text = item.text

        # Iterate and serialize all elements.
        for element in elements:
            self._serialize_element(element, node)

        # Return the node.
        return node

    def _serialize_element(self, element, parent=None):
        # Prepare the instance state for serialization.
        items = element.prepare(self)
        if not items:
            # No data to serialize; move along.
            return

        try:
            # Serialize the item(s).
            for item in items:
                parent.append(item.serialize())

        except TypeError:
            # Serialize the single item.
            parent.append(items.serialize())

    def serialize(self):
        """
        Serializes the data in the instance state as an
        XML representation.
        """

        # Serialize the root and return the serialized element.
        return self._serialize_item(self)

    def tostring(self):
        return etree.tostring(self.serialize())

    @classmethod
    def deserialize(cls, xml):
        # Instantiate an instance of ourself.
        instance = cls()

        # Set the text element if present.
        if xml.text:
            instance.text = xml.text

        # Iterate through the items and deserialize them on the instance.
        elements = iter(xml.getchildren())
        element = None
        index = 0
        items = list(cls._items.values())
        # print(items)
        while index < len(items):
            # Fetch the next item.
            item = items[index]
            index += 1

            if isinstance(item, Attribute):
                # Attempt to get the attribute from the
                # xml element.
                value = xml.attrib.get(item.name)

                # Clean the value using the item clean.
                value = item.clean(value)

                # Set it on the instance.
                item.__set__(instance, value)

            elif isinstance(item, Element):
                if element is None:
                    try:
                        # Get the next element in the chain.
                        element = next(elements)

                    except StopIteration:
                        break

                # Resolve the element into a schema object.
                obj = _element_registry.get(element.tag)
                if obj is None:
                    # Element is unknown; bail.
                    element = None
                    index -= 1
                    continue

                # Is this element a subclass of the current item?
                if not issubclass(obj, item.type):
                    # Nope; skip to the next item.
                    continue

                # Deserialize the element.
                value = obj.deserialize(element)

                # Set it on the instance.
                item.__set__(instance, value)

                # Are we dealing with a "collection" ?
                if item.collection:
                    index -= 1

                # Unset the current element reference.
                element = None

        # Return the deserialized instance.
        return instance

    @classmethod
    def fromstring(cls, text):
        return cls.deserialized(etree.XML(text))
