# -*- coding: utf-8 -*-
from werkzeug.exceptions import BadRequest

class RuleException(BadRequest):

    def __init__(self, rule, description=None, response=None):
        self.rule = rule
        super().__init__(description=description, response=response)

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [('Content-Type', 'text/html'),
                ('antlion-section', self.rule.section),
                ('antlion-message', self.description)]

    def __str__(self):
        return '%s --- %s' % (self.rule.section, self.description or '')

    def __repr__(self):
        return '%s --- %s' % (self.rule.section, self.description or '')
