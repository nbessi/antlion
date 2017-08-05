# -*- coding: utf-8 -*-
import os
from contextlib import contextmanager
import configparser
from httmock import HTTMock
from antlion.test import AntlionTestCase
from antlion.test import fake_reponse_content
from antlion.rule import RulesContext
from antlion.rule import BaseRule
from antlion import config
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


class ConfigTest(AntlionTestCase):

    @contextmanager
    def replace_config_file_candidates(self, path_list):
        original_list = path_list
        config.config_file_candidates = original_list = []
        try:
            yield
        except:
            raise
        finally:
            config.config_file_candidates = original_list

    def test_config_getter(self):
        """Test that an error is risen if no config file available"""

        os.environ['ANTLION_CONFIG_PATH'] = 'dummy'
        with self.assertRaises(config.ConfigurationError,
                               msg='Config error should be risen'):
            with self.replace_config_file_candidates([]):
                config.get_config()

    def test_config_from_environ(self):
        """Test reading file based of env variable"""
        config_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '..', 'config', 'antlion.ini')
        os.environ['ANTLION_CONFIG_PATH'] = config_path
        config_inst = config.get_config()
        self.assertTrue(isinstance(config_inst, configparser.ConfigParser))

    def test_config_validation(self):
        """Test validation of config file"""
        config_inst = configparser.ConfigParser()
        with self.assertRaises(config.ConfigurationError,
                               msg='Invalid config was validated'):
            config.validate_config(config_inst)

        config_inst = self.config
        config.validate_config(config_inst)
