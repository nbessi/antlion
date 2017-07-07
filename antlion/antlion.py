from werkzeug.datastructures import MultiDict
from flask import Flask, Response, request
from werkzeug.routing import Rule
import requests

app = Flask(__name__)
app.url_map.add(Rule('/<path:url>', endpoint='root'))
BLOCK_HEADERS = ['Host', 'Content-Length']


@app.endpoint('root')
def root(url):
    response = requests.request(
            method=request.method,
            url='http://' + url,
            stream=True,
            params=request.args,
            headers={k:v for k,v in request.headers if k not in BLOCK_HEADERS},
            data=request.get_data(),
            cookies=request.cookies)

    return Response(
            response.raw, # direct file interface
            headers=response.raw.headers.items(),
            status=response.status_code,
            direct_passthrough=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
