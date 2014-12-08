# -*- coding: utf-8 -*-
import re


def _upcase_first_letter(s):
    return s[0].upper() + s[1:]


def pascalize(name):
    name = _upcase_first_letter(name.strip())
    pattern = r'[-_\s]+(.)?'
    name = re.sub(pattern, lambda m: m.groups()[0].upper() if m else '', name)
    return name


class classproperty(object):
    """Declares a read-only `property` that acts on the class object.
    """

    def __init__(self, getter):
        self.getter = getter

    def __get__(self, obj, cls):
        return self.getter(cls)
