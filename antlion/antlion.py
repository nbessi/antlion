# -*- coding: utf-8 -*-
from urlparse import urlparse, urljoin

from werkzeug.datastructures import MultiDict
from flask import Flask, Response, request
from werkzeug.routing import Rule
import requests

app = Flask(__name__)
BLOCK_HEADERS = ['Host', 'Content-Length']
TARGET = urlparse('http://dummy_service:5500')

@app.route('/')
def root():
    import pdb; pdb.set_trace()
    url = urlparse(request.url)

    target_url =  url._replace(netloc=TARGET.netloc, scheme=TARGET.scheme)
    response = requests.request(
            method=request.method,
            url=target_url.geturl(),
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
