# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch
import configparser
from antlion.antlion import app
from httmock import all_requests
from werkzeug.test import EnvironBuilder


@all_requests
def response_content(url, request):
        return {'status_code': 200,
                'content': 'Antlion OK'}


def get_test_config():
    config = configparser.ConfigParser()
    config['antlion'] = {
        'endpoint': 'http://dummy_service:5500',
    }

    return config


class AntlionTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.config = get_test_config()
        with patch('antlion.config.get_config', side_effect=get_test_config):
            self.app = app.test_client()

    def create_environ(self, **kwargs):
        env_builder = EnvironBuilder(
            **kwargs,
        )
        return env_builder.get_environ()
