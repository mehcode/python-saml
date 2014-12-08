# -*- coding: utf-8 -*-
from .meta import version as VERSION
from .saml import *
from .samlp import *



def deserialize(xml):
    from .base import _element_registry

    # Resolve the xml into an element.
    element = _element_registry.get(xml.tag)
    if not element:
        return None

    # Deserialize the xml and return.
    return element.deserialize(xml)
