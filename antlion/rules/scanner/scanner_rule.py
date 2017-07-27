# -*- coding: utf-8 -*-
from antlion.rule import BaseRule
from antlion.errors import RuleException
from .data import KNOWN_USER_AGENTS


class ScannerDetection(BaseRule):

    section = 'REQUEST-913-SCANNER-DETECTION'

    description = """These rule will try to block scanner based on knowledge
    configuration"""
    priority = 5


    def __init__(self, config=None):
        super().__init__(config=config)
        self.block_empty_agent = config.getboolean('block_empty_agent')

    def check(self, request, logger=None):
        user_agent = request.headers.get('User-Agent')
        if not user_agent:
            if self.block_empty_agent:
                raise RuleException('Empty user agent')
            return
        for malicious_user_agent in KNOWN_USER_AGENTS:
            if malicious_user_agent.regexp.search(user_agent):
                raise RuleException(
                    self,
                    malicious_user_agent.desc
                )
