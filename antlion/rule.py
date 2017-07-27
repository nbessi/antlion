# -*- coding: utf-8 -*-
from importlib import import_module
from contextlib import contextmanager
import logging
from configparser import ConfigParser, SectionProxy
from heapq import heappush
from .errors import RuleException
RULE_LEVEL = 50

rules_class_register = []


def enable_rule_level():

    logging.addLevelName(RULE_LEVEL, "RULE")

    def rule(self, message, *args, **kws):
        # Yes, logger takes its '*args' as 'args'.
        if self.isEnabledFor(RULE_LEVEL):
            self._log(RULE_LEVEL, message, args, **kws)
    logging.Logger.rule = rule


def load_rules():
    import_module('.rules', 'antlion')


def register_class(cls):
    heappush(rules_class_register, cls)


class RuleMeta(type):

    section = None

    description = None

    priority = None

    def __new__(meta, name, bases, class_dict):
        if class_dict.get('priority') is None:
            class_dict['priority'] = 0
        cls = type.__new__(meta, name, bases, class_dict)
        if cls.__name__ != 'BaseRule':

            if class_dict.get('section') is None:
                raise NameError(
                    'Class {} section attribute must be set.'.format(
                        cls.__name__
                    )
                )
            if class_dict.get('description') is None:
                raise NameError(
                    'Class {} description attribute must be set.'.format(
                        cls.__name__
                    )
                )
            register_class(cls)
        return cls

    def __lt__(self, other):
        return self.priority < other.priority


class BaseRule(object, metaclass=RuleMeta):

    def __init__(self, config=None):
        if config is None:
            config = SectionProxy(ConfigParser(), self.section)
        self.config = config

    def check(self, request, logger=None):
        name = str(self)
        raise NotImplementedError(
            'Check method for {} must be implemented'.format(name)
        )

    def __repr__(self):
        return """{}
{}
priority: {}

{}""".format(self.section,
             "#" * len(self.section),
             self.priority,
             self.description)

    def __str__(self):
        return "{} -- priority: {}".format(self.section, self.priority)


class RulesContext(object):

    def __init__(self, config, logger):
        self.rules_register = []
        self.logger = logger
        for cls in rules_class_register:
            if cls.section in config:
                rule_config = config[cls.section]
                if rule_config.getboolean('disable'):
                    continue
                self.rules_register.append(cls(rule_config))
            else:
                self.rules_register.append(cls(config=None))

    def _check(self, rule, request, logger):
        rule.check(request, logger=logger)

    @contextmanager
    def check(self, request):
        try:
            for rule in self.rules_register:
                self._check(rule, request, self.logger)
            yield
        except RuleException as exc:
            rhash = hash(request)
            self.logger.rule('%s --- %s ', rhash, repr(request))
            self.logger.rule('%s --- %s',
                             rhash,
                             repr(exc))
            raise
        except Exception as exc:
            self.logger.error(repr(exc))
            raise
