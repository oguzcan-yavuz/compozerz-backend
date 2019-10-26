import os
import humps
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from composer import ComposerService


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
composerService = ComposerService()

# humps.camelize('jack_in_the_box')  # jackInTheBox
# humps.decamelize('rubyTuesdays')  # ruby_tuesdays
# humps.pascalize('red_robin')  # RedRobin


def format_composers(composers):
    return humps.camelize([format_composer(composer, ["bundle_path"]) for composer in composers])


def format_composer(composer, keys_to_delete=None):
    for key in keys_to_delete:
        del composer[key]


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
    return composerService.generate_melody(name)


if __name__ == "__main__":
    app.run()
