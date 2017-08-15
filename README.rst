ANTLION: A Python WSGI Web Application Firewall
###############################################

.. image:: https://travis-ci.org/nbessi/antlion.svg?branch=master
   :target: https://travis-ci.org/nbessi/antlion

.. image:: https://codecov.io/gh/nbessi/antlion/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/nbessi/antlion

Antlion is a modular Web Application FireWall written in Python.
It is based on Flask and is compatible with your favourite WSGI server.

Antlion is currently under heavy  development and his API is subject to change.

Why
===

Antlion was created because existing FOSS WAF are quite difficult to apprehend setup and extend.
The main objectives are:

* Provide an accessible set of core rules based on OWASP core rules.
* Provide a simple development framework to create dedicated rules set
* Allow flexible configuration based on standard python technology
* Be `SMART <https://en.wikipedia.org/wiki/SMART_criteria>`_
* Be scalable
* Allows fast prototyping

Setup
=====

Development
-----------

Antlion provides a Docker development that contains:

* An antlion service configured to run with gunicorn
* A simple dummy flask service that return the request received

First install `Docker <https://docs.docker.com/engine/installation/>`_ with `Docker Compose <https://docs.docker.com/compose/install/>`_

Then run following commands:

.. code-block:: bash

    git clone https://github.com/nbessi/antlion.git
    cd antlion
    docker-compose build --pull
    docker-compose up

if everything is OK, you should see the following output:

 .. code-block:: bash

    antlion_dummy_service_1 is up-to-date
    Starting antlion_waf_1
    Attaching to antlion_dummy_service_1, antlion_waf_1
    dummy_service_1  |  * Running on http://0.0.0.0:5500/ (Press CTRL+C to quit)
    dummy_service_1  |  * Restarting with stat
    dummy_service_1  |  * Debugger is active!
    dummy_service_1  |  * Debugger PIN: 271-297-553
    dummy_service_1  |  * Running on http://0.0.0.0:5500/ (Press CTRL+C to quit)
    dummy_service_1  |  * Restarting with stat
    dummy_service_1  |  * Debugger is active!


Press CTRL-C to stop the application.

to run antlion after editing some code:

.. code-block:: bash

    docker-compose run --rm -p5000:5000 waf


To do a simple test

.. code-block:: bash

   curl -A "nessus" -D - http://localhost:5000
   HTTP/1.1 400 BAD REQUEST
   Server: gunicorn/19.7.1
   Date: Thu, 27 Jul 2017 22:22:06 GMT
   Connection: close
   Content-Type: text/html
   antlion-section: REQUEST-913-SCANNER-DETECTION
   antlion-message: nessus vuln scanner
   Content-Length: 135

   <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
   <title>400 Bad Request</title>
   <h1>Bad Request</h1>
   <p>nessus vuln scanner</p>


We can see in the headers in case of violation antlion headers were added
and in the body the reasons

Production
----------

Install Python3 (I'll recommend Python 3.6 and higher),
`python-pip <https://pip.pypa.io/en/stable/installing/>`_ and optionally you can set up a Python virtualenv

Clone the package in the destination of your choice:


.. code-block:: bash

    git clone https://github.com/nbessi/antlion.git
    cd antlion
    python3 setup.py install --user
    # or globally
    sudo python3 setup.py install

Create a configuration file. Refer to the `Configuration` section.

You can now bind the `antlion.antlion:app` to your preferred WSGI server.

I recommend `Gunicorn <http://docs.gunicorn.org/en/stable/deploy.html>`_ with Gevent.
As the application act as a proxy you want to avoid timeout.

Configuration
=============

Antlion setup is based on a `ConfigParser <https://docs.python.org/3/library/configparser.html#ConfigParser.SafeConfigParser>`_ configuration files.

You will find a complete configuration sample file under the `config folder <https://github.com/nbessi/antlion/tree/master/config>`_

The configuration file must be named `antlion.ini` and must be
located in one of the following locations:

* `~`
* `etc/`

or the path to the configuration file can be set via an environment variable `ANTLION_CONFIG_PATH`

Main Section
------------

The `[antlion]` configuration section is mandatory.
It musts contain the proxy endpoint

.. code-block:: text

    [antlion]
    endpoint = http://dummy_service:5500

Rules Setup
-----------

Each rule can be provided with it own configuration.
To do this the section name of the configuration file must match the section property of the rule class:

.. code-block:: python

    class ScannerDetection(BaseRule):

        section = 'REQUEST-913-SCANNER-DETECTION'


The section will be reflected in the config file if needed:

.. code-block:: text

    [REQUEST-913-SCANNER-DETECTION]
    block_empty_agent = yes

You will find all section in the core rule documentation.

There is a common option 'disable' that can be set in a section to
disable the loading and evaluation of a rule.

Logging
-------

In a WAF logging is important that why Antlion tries to provide the most flexible approach
to logging.

If nothing is set in config file Antlion will use the default Flask logger to level INFO.
If you provide `FileConfig` required section you will be able to freely setup your
logging policy (stream, file, rotating file, mail, etc) please see `related documentation <https://docs.python.org/3/library/logging.config.html#logging-config-fileformat>`_

Antlion also provides a `RULE` log level associated with a `Logger.rule` function


Developing a rule
==================

Developing a rule is a straight forward process.
Simply create a module and create a class that derived from `antlion.rule.BaseRule`
A rule is automatically registered when the sub class of `antlion.rule.BaseRule` is instantiated


.. code-block:: python

    # -*- coding: utf-8 -*-
    from antlion.rule import BaseRule
    from antlion.errors import RuleException

    class ScannerDetection(BaseRule):


        section = 'REQUEST-913-SCANNER-DETECTION' # OWASP section and code

        description = """These rule will try to block scanner based on knowledge configuration"""

        priority = 5


        def __init__(self, config=None):
            super().__init__(config=config)
            self.block_empty_agent = self.config.getboolean('block_empty_agent')

        def check(self, request, logger=None):
            user_agent = request.headers.get('User-Agent')
            if not user_agent:
                if self.block_empty_agent:
                    raise RuleException(self, 'Empty user agent')
                return
            for malicious_user_agent in KNOWN_USER_AGENTS:
                if malicious_user_agent.regexp.search(user_agent):
                    raise RuleException(
                        self,
                        malicious_user_agent.desc
                    )


The class has mandatory properties:

 * `section`: a string describing the rule it should be composed like `DOMAIN_OWASPCODE_DESCRIPTION`
 * `description`: a string describing the rule behavior
 * `priority`: (set by default to 0) it will determine the priority of the rule. A small values means higher priority

A rule also receives in his constructor his corresponding configparser section and a logger.
They can be accessed via `self.config` and `self.logger`


When an antlion security context manager is called it will iterate over all rules.
When processing a rule the security context manager will call the rule `check` method and pass the current `werkzeug request <http://werkzeug.pocoo.org/docs/0.12/wrappers/>`_ and the context logger.

The check function must return an `antlion.errors.RuleException` in case of rule violation.

The Exception needs to receive the rule and a message as parameters.
When such an error is raised it will alter response header and set response code to 400 bad request.

Testing your rule
-----------------

Antlion provide facilities to test your rule. In a test folder create a module starting with `test_` or matching your test tools pattern.
The `AntlionTestCase` base class provide:

 * A helper to create Werkzeug `EnvironBuilder` `create_environ`
 * A test config and a test logger `self.config`, `self.logger`

and some less common helpers used to test the antlion core:

 * A helper to get a flask test client with patched config `get_antlion_client`
 * A helper to mock `requests` proxy response `fake_reponse_content`

When the test class setup herself it will empty the rule class register allowing you to test only the current rules.


.. code-block:: python

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


Extending core rules
--------------------

If you want to extend core rules, you must add a package in `antlion.rules <https://github.com/nbessi/antlion/tree/master/antlion/rules>`_ and load your package in the `__init__.py`.
You must also add test cases in the test folder. The directory structure must reflect the rules package.

Packaging your own rule
-----------------------

You can create your own rules eggs.
The only prerequisite are:

 * Depending on antlion
 * Loading/importing your rule class in order to have them registered

I recommend following `Kenneth Reitz recommendations <https://www.kennethreitz.org/essays/repository-structure-and-python>`_

Roadmap
=======

short term
----------

* Finalise first version of API
* Provide a decent set of core rules
* Setup test logic and API
* Do the first release (package, doc, etc)


Middle term
-----------

* Provide data persistency
* Provide advance rules
* Organise rules in wheels

Long term
---------
* provide admin interface
* native reporting


API documentation
=================

Todo
