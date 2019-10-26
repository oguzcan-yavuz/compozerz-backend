import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from composer import ComposerService


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
composerService = ComposerService()


@app.route("/")
def hello():
    return jsonify({ "message": "Hello World!" })


@app.route("/composer/<name>/generate", methods=["POST"])
def hello_name(name):
    return composerService.generate_melody(name)


if __name__ == "__main__":
    app.run()
