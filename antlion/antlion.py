from urllib.parse import urlparse
from flask import Response, request, Flask
import requests
import rules_lib
import config


app = Flask(__name__)
with app.app_context():
    config = config.get_config()
    app.config.update(config)
    app.config.update(config['antlion'])
    if 'flask' in config:
        app.config.update(config['flask'])
ENDPOINT = urlparse(app.config['endpoint'])


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def root(path):
    url = urlparse(request.url)
    for rule_context in rules_lib.base_rule.rules_registery:
        print(repr(rule_context))
    target_url = url._replace(netloc=ENDPOINT.netloc, scheme=ENDPOINT.scheme)
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
    # app.run(host="0.0.0.0", debug=True, passthrough_errors=False, port=5000)

    from gevent.wsgi import WSGIServer
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
