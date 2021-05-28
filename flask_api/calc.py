#!/usr/bin/env python3

from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/sum/')
def hello():
    a = int(request.args.get("a"))
    b = int(request.args.get("b"))
    return f'Answer is: {a+b}'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
