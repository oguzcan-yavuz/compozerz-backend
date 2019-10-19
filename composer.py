import os
import constants as Constants
import magenta.music as mm
import magenta
import tensorflow


class ComposerService:
    def __init__(self):
        # COMPOSERS = [{ name: '', midi_path: '', model_path: ''}]
        # TODO: move generating things we can generate to init and add if exists control
        self.COMPOSERS = []
        self.create_composers(Constants.DATA_PATH)


    def create_composers(self, path):
        for _, dirs, _ in os.walk(path):
            for dir in dirs:
                composer_path = os.path.join(path, dir)
                midi_path = os.path.join(composer_path, "midi")
                tfrecord_path = os.path.join(composer_path, "notesequences.tfrecord")
                melody_rnn_path = os.path.join(composer_path, "melody_rnn")
                sequence_examples_path = os.path.join(melody_rnn_path, "sequence_examples")
                composer = {
                    "name": dir,
                    "paths": {
                        "midi": midi_path,
                        "tfrecord": tfrecord_path,
                        "melody_rnn": melody_rnn_path,
                        "sequence_examples": sequence_examples_path,
                    },
                }
                self.COMPOSERS.append(composer)


    def get_composers(self):
        return self.COMPOSERS


    def get_composer_by_name(self, name):
        return next((composer for composer in self.COMPOSERS if composer["name"] == name), None)


    def create_tfrecord(self, composer):
        # convert_dir_to_note_sequences \
        # --input_dir=$INPUT_DIRECTORY \
        # --output_file=$SEQUENCES_TFRECORD \
        # --recursive
        midi_path = composer["paths"]["midi"]
        tfrecord_path = composer["paths"]["tfrecord"]

        os.system(
            "convert_dir_to_note_sequences --input_dir={0} --output_file={1} --recursive"
                .format(midi_path, tfrecord_path)
        )


    def create_sequence_examples(self, composer):
        # melody_rnn_create_dataset \
        #     --config=<one of 'basic_rnn', 'mono_rnn', lookback_rnn', or 'attention_rnn'> \
        #     --input=/tmp/notesequences.tfrecord \
        #     --output_dir=/tmp/melody_rnn/sequence_examples \
        #     --eval_ratio=0.10
        config = Constants.RNN_CONFIG
        eval_ratio = Constants.EVAL_RATIO
        tfrecord_path = composer["paths"]["tfrecord"]
        sequence_examples_path = composer["paths"]["sequence_examples"]

        os.system(
            "melody_rnn_create_dataset --input_dir={0} --output_file={1} --config={2} --eval_ratio={3}"
                .format(tfrecord_path, sequence_examples_path, config, eval_ratio)
        )


    def train_composer(self, name):
        composer = self.get_composer_by_name(name)
        return composer


    def generate_melody(self, name, input_melody):
        pass
