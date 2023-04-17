import os
import humps
import base64
from flask import Flask, request, jsonify, Response, send_file
from flask_cors import CORS, cross_origin
from composer import ComposerService
from magenta.music.protobuf import music_pb2


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


@app.route("/composers/", methods=["GET"])
def get_composers():
    composers = composerService.get_composers()
    formatted_composers = format_composers(composers)
    return jsonify(formatted_composers)


@app.route("/composers/<name>/generate", methods=["POST"])
def generate(name):
    composer_name = name.lower()
    print("yvz here:")
    print(request.json['noteSequence'])

    seq = music_pb2.NoteSequence()

    for note in request.json['noteSequence']['notes']:
        seq.notes.add(pitch=note['pitch'], start_time=note['startTime'], end_time=note['endTime'], velocity=note['velocity'])

    for tempo in request.json['noteSequence']['tempos']:
        seq.tempos.add(qpm=tempo['qpm'])

    midi_path = composerService.generate_melody(composer_name, seq)
    return send_file(midi_path, mimetype='audio/midi')


if __name__ == "__main__":
    app.run()
