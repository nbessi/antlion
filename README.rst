ANTLION: A Python WSGI Web Application Firewall
###############################################

.. image:: https://travis-ci.org/nbessi/antlion.svg?branch=master
   :target: https://travis-ci.org/nbessi/antlion

.. image:: https://codecov.io/gh/nbessi/antlion/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/nbessi/antlion

Antlion is a modular Web Application FireWall written in Python.
It is based on Flask and is compatible with your favorite WSGI server.

Antlion is currently under heavy developpement and his API is subject to change.

Why
===

Antlion was created because existing FOSS WAF are quite difficult to apprehend setup and extend.
The main objectives are:

* Provide an accessible set of core rules based on owasp core rules.
* Provide a simple developpement framework to create dedicated rules set
* Allow flexible configuration based on standard python technology
* Be `SMART <https://en.wikipedia.org/wiki/SMART_criteria>`_
* Be scalable
* Allows fast protoyping

Setup
=====

Development
-----------

Antlion provide a Docker development that contains:

* An antlion service configured to run with gunicorn
* A simple dummy flask service that return the request recieved

First install `Docker <https://docs.docker.com/engine/installation/>`_ with `Docker Compose <https://docs.docker.com/compose/install/>`_

Then run following commands:

.. code-block:: bash

    git clone https://github.com/nbessi/antlion.git
    cd antlion
    docker-compose build --pull
    docker-compose up

if everything is OK you should see the following output:

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


press CTRL-C to stop the application.

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


We can see in the headers in case of violation antlion headers where added
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

You can now bind the `antlion.antlion:app` to your prefered WSGI server.

I recommend `Gunicorn <http://docs.gunicorn.org/en/stable/deploy.html>`_ with Gevent.
As the application act as a proxy you want to avoid timeout.

Configuration
=============

Antlion setup is based on a `ConfigParser <https://docs.python.org/3/library/configparser.html#ConfigParser.SafeConfigParser>`_ configuration files.

You will find an complete configuration sample file under the `config folder <https://github.com/nbessi/antlion/tree/master/config>`_

The configuration file must be name `antlion.ini` and must be
located in one of the following location:

* `~`
* `etc/`

or the path to the conif file can be set via an environment variable `ANTLION_CONFIG_PATH`

Main Section
------------

The `[antlion]` configuration section is mandatory.
It musts contains the proxy endpoint

.. code-block:: text

    [antlion]
    endpoint = http://dummy_service:5500

Rules Setup
-----------

Each rules can be provided with it own configuration.
To do this the section name of the configfile must match the section property of the rule class:

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

In a WAF logging is important that why Antlion tries to provides the most flexible approach
to logging.

If nothing is set in config file Antlion will use the default Flask logger to level INFO.
If you provide `FileConfig` required section you will be able to freely setup your
logging policy (stream, file, rotating file, mail, etc) please see `related documentation <https://docs.python.org/3/library/logging.config.html#logging-config-fileformat>`_

Antlion also provides a `RULE` log level associatied with a `Logger.rule` function


Developping a rule
==================

Todo


Roadmap
=======

short term
----------

* Finalize first version of API
* Provide a decent set of core rules
* Setup test logic and API
* Do the first release (package, doc, etc)


Middle term
-----------

* Provide data persitency
* Provide advance rules
* Organize rules in wheels

Long term
---------
* provide admin interface
* native reporting


API documentation
=================

Todo
