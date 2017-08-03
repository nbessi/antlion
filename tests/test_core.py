# -*- coding: utf-8 -*-
import logging
from antlion.test import AntlionTestCase
from antlion.rule import RulesContext
from antlion.rule import BaseRule
from antlion.errors import RuleException
from werkzeug.wrappers import Request

class DummyRule(BaseRule):

    section = 'ANTLION-TEST'

    description = "Dummy test rule"
    priority = 5

    def __init__(self, config=None):
        super().__init__(config=config)
        self.should_raise = True

    def check(self, request, logger=None):
        if self.should_raise:
            raise RuleException(
                self,
                'Test Rule positive'
            )


class CoreTest(AntlionTestCase):

    def setUp(self):
        super().setUp()
        self.env = self.create_environ(
            method='POST',
            data={'dummy': 'test'}
        )
        self.w_request = Request(self.env)
        self.register_rule(DummyRule)

    def test_context_init(self):
        """Test rule context initalisation"""
        rules_context = RulesContext(self.config, logging.getLogger())
        self.assertEqual(len(rules_context.rules_register), 1)
        self.assertIsInstance(rules_context.rules_register[0], DummyRule)

    def test_context_check(self):
        """Test evaluation of test rules"""
        rules_context = RulesContext(self.config, logging.getLogger())
        self.assertTrue(hasattr(rules_context.rules_register[0],
                                'should_raise'))
        with self.assertRaises(RuleException, msg='Exception should be risen'):
            with rules_context.check(self.w_request):
                print('test RulesContext Core')

        rules_context.rules_register[0].should_raise = False
        try:
            with rules_context.check(self.w_request):
                print('test RulesContext Core')
        except RuleException:
            self.fail('Exception risen when it should not')
