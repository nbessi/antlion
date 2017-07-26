# -*- coding: utf-8 -*-
from heapq import heappush

rules_registery = []


def register_class(cls):
    heappush(rules_registery, cls)


class RuleMeta(type):

    owasp_section = None

    owasp_description = None

    priority = None

    def __new__(meta, name, bases, class_dict):
        if class_dict.get('priority') is None:
            class_dict['priority'] = 0
        cls = type.__new__(meta, name, bases, class_dict)
        if cls.__name__ != 'BaseRule':

            if class_dict.get('owasp_section') is None:
                raise NameError(
                    'Class {} owasp_section attribute must be set.'.format(
                        cls.__name__
                    )
                )
            if class_dict.get('owasp_description') is None:
                raise NameError(
                    'Class {} owasp_description attribute must be set.'.format(
                        cls.__name__
                    )
                )
            register_class(cls)
        return cls

    def __lt__(self, other):
        return self.priority < other.priority

    def __repr__(self):
        return """{}
{}
priority: {}

{}""".format(self.owasp_section,
             "#" * len(self.owasp_section),
             self.priority,
             self.owasp_description)

    def __str__(self):
        return "{} -- priority: {}".format(self.owasp_section, self.priority)


class BaseRule(object, metaclass=RuleMeta):

    def check(self, request):
        raise NotImplemented(
            'Check method for {} must be implemented'.format(self)
        )

    def __init__(self, config=None):
        if config is None:
            config = {}
        self.config = config
