# -*- coding: utf-8 -*-
from flask import Flask, render_template, send_from_directory


app = Flask(__name__)

@app.route("/")
def download(filename="test.pdf"):
    return send_from_directory("", filename)

if __name__ == '__main__':
    app.run("0.0.0.0","8000",debug=True)
