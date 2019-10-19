import os
import constants as Constants


class ComposerService:
    def __init__(self):
        # COMPOSERS = [{ name: '', midi_path: '', model_path: ''}]
        self.COMPOSERS = []
        self.create_composers(Constants.MIDI_PATH)


    def create_composers(self, path):
        for _, dirs, _ in os.walk(path):
            for dir in dirs:
                composer_path = os.path.join(path, dir)
                composer = {
                    "name": dir,
                    "midi_path": composer_path,
                    "model_path": ''
                }
                self.COMPOSERS.append(composer)


    def get_composers(self):
        return self.COMPOSERS


    def get_composer_by_name(self, name):
        return next((composer for composer in self.COMPOSERS if composer["name"] == name), None)


    def train_composer(self, name):
        pass


    def generate_melody(self, name, input_melody):
        pass
