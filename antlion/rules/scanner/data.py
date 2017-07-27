# -*- coding: utf-8 -*-
import re
from collections import namedtuple
UserAgent = namedtuple('UserAgent', ['regexp', 'desc'])
KNOWN_USER_AGENTS = [
    UserAgent(re.compile(r'\(hydra\)'),
              'Hydra password cracker http://sectools.org/tool/hydra/'),

    UserAgent(re.compile(r'absinthe'),
              'absinthe sql injection'),

    UserAgent(re.compile(r'advanced email extractor'),
              'Advance mail extractor'),

    UserAgent(re.compile(r'arachni'),
              'Arachni Scanner'),

    UserAgent(re.compile(r'autogetcontent'),
              'Autogetcontent'),

    UserAgent(re.compile(r'bilbo'),
              'Bilbo'),

    UserAgent(re.compile(r'BFAC'),
              'Backup File Artifacts https://github.com/mazen160/bfac'),

    UserAgent(re.compile(r'brutus'),
              'Brutus cracker'),

    UserAgent(re.compile(r'brutus'),
              'brutus/aet'),

    UserAgent(re.compile(r'bsqlbf'),
              'bsqlbf brute force'),

    UserAgent(re.compile(r'cgichk'),
              'cgichk vuln scanner'),

    UserAgent(re.compile(r'cisco-torch'),
              'cisco-torch vuln scranner'),

    UserAgent(re.compile(r'commix'),
              'commix vuln scranner'),

    UserAgent(re.compile(r'core-project'),
              'core-projecg vuln scranner'),

    UserAgent(re.compile(r'crimscanner'),
              'crimscanner vuln scranner'),

    UserAgent(re.compile(r'datacha0s'),
              'datacha0s vuln scranner'),

    UserAgent(re.compile(r'dirbuster'),
              'dirbuster scrapper'),

    UserAgent(re.compile(r'dominohunter'),
              'domino hunter vul scanner'),

    UserAgent(re.compile(r'dotdotpwn'),
              'dotdopwn hunter vul scanner'),

    UserAgent(re.compile(r'email extractor'),
              'email extractor'),

    UserAgent(re.compile(r'fhscan'),
              'fhscan'),

    UserAgent(re.compile(r'floodgate'),
              'floodgate'),

    UserAgent(re.compile(r'get-minimal'),
              'get-minimal'),

    UserAgent(re.compile(r'gootkit'),
              'gootkit vuln scanner'),

    UserAgent(re.compile(r'auto-rooter'),
              'gootkit vuln scanner'),

    UserAgent(re.compile(r'scanner'),
              'Generic scanner'),

    UserAgent(re.compile(r'grabber'),
              'Grabber'),

    UserAgent(re.compile(r'grendel-scan'),
              'Grendel vuln scanner'),

    UserAgent(re.compile(r'havij'),
              'havij sql injection'),

    UserAgent(re.compile(r'inspath'),
              'inspath vuln scanner'),

    UserAgent(re.compile(r'jaascois'),
              'jaascois vuln scanner'),

    UserAgent(re.compile(r'internet ninja'),
              'Internet ninja vuln scanner'),

    UserAgent(re.compile(r'zmeu'),
              'zmeu vuln scanner'),

    UserAgent(re.compile(r'masscan'),
              'masscan port scanner'),

    UserAgent(re.compile(r'metis'),
              'metis vuln scanner'),

    UserAgent(re.compile(r'morfeus'),
              'Morfeus vuln scanner'),

    UserAgent(re.compile(r'mysqloit'),
              'mysqloit sql injection'),

    UserAgent(re.compile(r'n-stealth'),
              'n-stealth vuln scanner'),

    UserAgent(re.compile(r'nessus'),
              'nessus vuln scanner'),

    UserAgent(re.compile(r'netsparker'),
              'netsparker vuln scanner'),

    UserAgent(re.compile(r'nikto'),
              'nikto vuln scanner'),

    UserAgent(re.compile(r'nmap'),
              'nmap scanner'),

    UserAgent(re.compile(r'nse'),
              'nmap scanner'),

    UserAgent(re.compile(r'nsauditor'),
              'nsauditor scanner'),

    UserAgent(re.compile(r'openvas'),
              'OpenVAS'),

    UserAgent(re.compile(r'pangolin'),
              'Pangolin vuln scanner'),

    UserAgent(re.compile(r'paros'),
              'Paros vuln scanner'),

    UserAgent(re.compile(r'pmafind'),
              'PHP my admin scanner'),

    UserAgent(re.compile(r'customcrawler'),
              'customcrawler'),

    UserAgent(re.compile(r'qualys was'),
              'qualys vuln scanner'),

    UserAgent(re.compile(r's\.t\.a\.l\.k\.e\.r'),
              's.t.a.l.k.e.r'),

    UserAgent(re.compile(r'security scan'),
              'security scan'),

    UserAgent(re.compile(r'springenwerk'),
              'springenwerk vuln scanner'),

    UserAgent(re.compile(r'sql power injector'),
              'SQL power injector'),

    UserAgent(re.compile(r'sqlmap'),
              'SQLMap'),

    UserAgent(re.compile(r'sqlninja'),
              'sqlninja'),

    UserAgent(re.compile(r'(teh|forest|lobster)'),
              'Medusa password cracker'),

    UserAgent(re.compile(r'this is an exploit'),
              'This is an exploit common message'),

    UserAgent(re.compile(r'(toata|dragostea|mea|pentru|diavola)'),
              'Taoata familly scanner'),

    UserAgent(re.compile(r'uil2pn'),
              'Cisco uil2pn SQL bot'),

    UserAgent(re.compile(r'vega'),
              'Vega vuln scanner'),

    UserAgent(re.compile(r'voideye'),
              'Voideye'),

    UserAgent(re.compile(r'w3af'),
              'w3af'),

    UserAgent(re.compile(r'webbandit'),
              'webbandit'),

    UserAgent(re.compile(r'webinspect'),
              'webinspect vuln scanner'),

    UserAgent(re.compile(r'webshag'),
              'webshag site scanner'),

    UserAgent(re.compile(r'webtrends'),
              'webtrends site scanner'),

    UserAgent(re.compile(r'webvulnscan'),
              'webvulnscan vuln scanner'),

    UserAgent(re.compile(r'whatweb'),
              'Whatweb'),

    UserAgent(re.compile(r'whcc'),
              'whcc'),

    UserAgent(re.compile(r'wordpress hash grabber'),
              'wordpress hash grabber'),

    UserAgent(re.compile(r'xmlrpc exploit'),
              'xmlrpc exploit'),

    UserAgent(re.compile(r'WPScan'),
              'WordPress Scan wpscan.org'),
]
