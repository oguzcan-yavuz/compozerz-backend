import os
import humps
import base64
from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
from composer import ComposerService


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
composerService = ComposerService()


def format_composers(composers):
    return humps.camelize([format_composer(composer, ["bundle_path"]) for composer in composers])


def format_composer(composer, keys_to_delete=None):
    for key in keys_to_delete:
        del composer[key]
    return composer


@app.route("/")
def hello():
    return jsonify({ "message": "Hello World!" })


@app.route("/composers/", methods=["GET"])
def get_composers():
    composers = composerService.get_composers()
    formatted_composers = format_composers(composers)
    return jsonify(formatted_composers)


@app.route("/composers/<name>/generate", methods=["POST"])
def generate(name):
    composer_name = name.lower()
    midi_path = composerService.generate_melody(composer_name)
    with open(midi_path, "rb") as midi:
        encoded_midi = base64.b64encode(midi.read())
        print('encoded_midi: {0}'.format(encoded_midi))
        return encoded_midi


if __name__ == "__main__":
    app.run()
