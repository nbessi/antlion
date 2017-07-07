from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def hello_world():
    return request.url


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5500)
