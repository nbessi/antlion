# -*- coding: utf-8 -*-
from contextlib import contextmanager
from httmock import HTTMock
from antlion.test import AntlionTestCase
from antlion.test import fake_reponse_content
from antlion.rule import RulesContext
from antlion.rule import BaseRule
from antlion.errors import RuleException
from antlion import antlion
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

    @contextmanager
    def replace_antlion_register(self, register):
        original_register = antlion.rules_context.rules_register
        antlion.rules_context.rules_register = register
        try:
            yield
        except:
            raise
        finally:
            antlion.rules_context.rules_register = original_register

    def test_context_init(self):
        """Test rule context initalisation"""
        rules_context = RulesContext(self.config, self.logger)
        self.assertEqual(len(rules_context.rules_register), 1)
        self.assertIsInstance(rules_context.rules_register[0], DummyRule)

    def test_context_check(self):
        """Test evaluation of test rules"""
        rules_context = RulesContext(self.config, self.logger)
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


    def test_proxy(self):
        """Test good behavior of waf proxy"""
        rule = DummyRule(self.config)
        rule.should_raise = False
        with self.replace_antlion_register([rule]):
            with HTTMock(fake_reponse_content):
                client = self.get_antlion_client()
                res = client.get('/nbessi/antlion')
            self.assertEqual(res.status_code, 200)


    def test_proxy_interception(self):
        """Test good behavior of response when rule error is triggered"""
        rule = DummyRule(self.config)
        rule.should_raise = True
        with self.replace_antlion_register([rule]):
            with HTTMock(fake_reponse_content):
                client = self.get_antlion_client()
                res = client.get('/nbessi/antlion')

            self.assertEqual(res.status_code, 400)
            self.assertTrue(res.headers.get('antlion-message'))
