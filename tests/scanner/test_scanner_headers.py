# -*- coding: utf-8 -*-
from werkzeug.wrappers import Request
from antlion.test import AntlionTestCase
from antlion.rule import RulesContext
from antlion.rules.scanner.scanner_header_rule import ScannerDetection
from antlion.errors import RuleException


class ScannerHeaderTest(AntlionTestCase):
    """Test black list detection of scanner user agent"""

    def setUp(self):
        super().setUp()
        self.env = self.create_environ(
            method='POST',
            data={'dummy': 'test'},
            headers={'User-Agent': 'Mozilla'},
        )
        self.register_rule(ScannerDetection)

    def test_valid_request(self):
        """Test a valid request"""
        request = Request(self.env)

        rules_context = RulesContext(self.config, self.logger)
        try:
            with rules_context.check(request):
                print('Test scanner header detection')
        except RuleException:
            self.fail('False positive for scanner header')

    def test_invalid_request(self):
        """Test detection of scanner header"""
        self.env['HTTP_USER_AGENT'] = 'nessus'
        request = Request(self.env)

        rules_context = RulesContext(self.config, self.logger)

        with self.assertRaises(RuleException,
                               msg='False negative for scanner header'):
            with rules_context.check(request):
                print('Test scanner header detection')

    def test_empty_agent(self):
        """Test detection of emtpy_agent"""
        self.env['HTTP_USER_AGENT'] = ''
        request = Request(self.env)
        self.config.add_section('REQUEST-913-SCANNER-DETECTION')
        self.config['REQUEST-913-SCANNER-DETECTION']['block_empty_agent'] = 'yes'
        rules_context = RulesContext(self.config, self.logger)

        with self.assertRaises(RuleException,
                               msg='False negative for empty agent'):
            with rules_context.check(request):
                print('Test empty agent')
