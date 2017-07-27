# -*- coding: utf-8 -*-
import logging
from logging.config import fileConfig
from urllib.parse import urlparse
from flask import Response, request, Flask
import requests
from .rule import RulesContext, load_rules, enable_rule_level
from . import config

enable_rule_level()
load_rules()

app = Flask('antlion')
app.logger_name = 'antlion_default'
with app.app_context():
    antlion_config = config.get_config()
    app.config.update(antlion_config)
    app.config.update(antlion_config['antlion'])
    log = None
    if 'flask' in antlion_config:
        app.config.update(antlion_config['flask'])
    if 'loggers' in antlion_config:
        app.logger
        app.logger.setLevel(10)
        fileConfig(antlion_config)
        root = logging.getLogger()
        log = logging.getLogger('antlion')
        app.logger.addHandler(log)
    else:
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)

rule_context = RulesContext(antlion_config, log or app.logger)
ENDPOINT = urlparse(app.config['endpoint'])


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def root(path):
    with rule_context.check(request):
        url = urlparse(request.url)
        target_url = url._replace(netloc=ENDPOINT.netloc,
                                  scheme=ENDPOINT.scheme)
        response = requests.request(
                method=request.method,
                url=target_url.geturl(),
                stream=True,
                params=request.args,
                headers=request.headers,
                data=request.get_data(),
                cookies=request.cookies)

        return Response(
                response.raw,  # direct file interface
                headers=response.raw.headers.items(),
                status=response.status_code,
                direct_passthrough=True)


if __name__ == "__main__":
    from gevent.wsgi import WSGIServer
    from werkzeug.debug import DebuggedApplication
    http_server = WSGIServer(('', 5000), DebuggedApplication(app))
    http_server.serve_forever()
