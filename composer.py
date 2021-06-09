import os
import copy
import constants as Constants
import magenta.music as mm
from magenta.models.shared import sequence_generator_bundle
import magenta
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.music.protobuf import generator_pb2
from magenta.music.protobuf import music_pb2
from magenta.music import midi_synth
from magenta.music import midi_io
import tensorflow

twinkle_twinkle = music_pb2.NoteSequence()

# Add the notes to the sequence.
twinkle_twinkle.notes.add(pitch=60, start_time=0.0, end_time=0.5, velocity=80)
twinkle_twinkle.notes.add(pitch=60, start_time=0.5, end_time=1.0, velocity=80)
twinkle_twinkle.notes.add(pitch=67, start_time=1.0, end_time=1.5, velocity=80)
twinkle_twinkle.notes.add(pitch=67, start_time=1.5, end_time=2.0, velocity=80)
twinkle_twinkle.notes.add(pitch=69, start_time=2.0, end_time=2.5, velocity=80)
twinkle_twinkle.notes.add(pitch=69, start_time=2.5, end_time=3.0, velocity=80)
twinkle_twinkle.notes.add(pitch=67, start_time=3.0, end_time=4.0, velocity=80)
twinkle_twinkle.notes.add(pitch=65, start_time=4.0, end_time=4.5, velocity=80)
twinkle_twinkle.notes.add(pitch=65, start_time=4.5, end_time=5.0, velocity=80)
twinkle_twinkle.notes.add(pitch=64, start_time=5.0, end_time=5.5, velocity=80)
twinkle_twinkle.notes.add(pitch=64, start_time=5.5, end_time=6.0, velocity=80)
twinkle_twinkle.notes.add(pitch=62, start_time=6.0, end_time=6.5, velocity=80)
twinkle_twinkle.notes.add(pitch=62, start_time=6.5, end_time=7.0, velocity=80)
twinkle_twinkle.notes.add(pitch=60, start_time=7.0, end_time=8.0, velocity=80) 
twinkle_twinkle.total_time = 8

twinkle_twinkle.tempos.add(qpm=60);


class ComposerService:
    def __init__(self):
        # COMPOSERS = [{ name: "", bundle_path: ""}]
        self.COMPOSERS = []
        self.init_composers(Constants.DATA_PATH)


    def init_composers(self, path):
        for composer_name in os.listdir(path):
            if not composer_name.startswith('.'):
                bundle_path = os.path.join(path, composer_name, "basic_rnn.mag")
                composer = {
                    "name": composer_name,
                    "bundle_path": bundle_path,
                }
                self.COMPOSERS.append(composer)


    def get_composers(self):
        return copy.deepcopy(self.COMPOSERS)


    def get_composer_by_name(self, name):
        return next((composer for composer in self.COMPOSERS if composer["name"] == name), None)


    def generate_melody(self, name, input_sequence=twinkle_twinkle):
        composer = self.get_composer_by_name(name)
        if composer is None:
            raise Exception('composer not found')
        bundle = sequence_generator_bundle.read_bundle_file(composer["bundle_path"])
        generator_map = melody_rnn_sequence_generator.get_generator_map()
        melody_rnn = generator_map["basic_rnn"](checkpoint=None, bundle=bundle)
        melody_rnn.initialize()
        num_steps = 128 # change this for shorter or longer sequences
        temperature = 1.0 # the higher the temperature the more random the sequence.

        # Set the start time to begin on the next step after the last note ends.
        last_end_time = (max(n.end_time for n in input_sequence.notes)
                        if input_sequence.notes else 0)
        qpm = input_sequence.tempos[0].qpm 
        seconds_per_step = 60.0 / qpm / melody_rnn.steps_per_quarter
        total_seconds = num_steps * seconds_per_step

        generator_options = generator_pb2.GeneratorOptions()
        generator_options.args["temperature"].float_value = temperature
        generate_section = generator_options.generate_sections.add(
        start_time=last_end_time + seconds_per_step,
        end_time=total_seconds)

        # Ask the model to continue the sequence.
        sequence = melody_rnn.generate(input_sequence, generator_options)
        midi_path = 'tmp.mid'
        midi_io.note_sequence_to_midi_file(sequence, midi_path)
        return midi_path
