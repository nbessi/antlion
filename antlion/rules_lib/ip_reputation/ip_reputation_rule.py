# -*- coding: utf-8 -*-
from ..base_rule import BaseRule


class IpReputation(BaseRule):
    """These rules deal with detecting traffic from IPs that have previously been involved with malicious activity
    either on our local site or globally."""
    owasp_section = 'REQUEST-10-IP-REPUTATION'
    owasp_description = __doc__
    priority = 10
