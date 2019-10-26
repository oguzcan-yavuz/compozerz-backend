#!/usr/bin/bash

DATA_PATH=./data/*

for COMPOSER_PATH in $DATA_PATH;
    do
        COMPOSER="$(basename "$COMPOSER_PATH")"
        MIDI_PATH="$COMPOSER_PATH/midi"
        TFRECORD_PATH="$COMPOSER_PATH/notesequences.tfrecord"
        MELODY_RNN_PATH="$COMPOSER_PATH/melody_rnn"
        DATASET_PATH="$MELODY_RNN_PATH/sequence_examples"
        TRAINING_PATH="$DATASET_PATH/training_melodies.tfrecord"
        RUN_PATH="$MELODY_RNN_PATH/logdir/run1"
        CONFIG="basic_rnn"
        EVAL_RATIO=0.10
        HPARAMS="batch_size=64,rnn_layer_sizes=[64,64]"
        TRAINING_STEPS=20000
        BUNDLE_FILE="$COMPOSER_PATH/$CONFIG.mag"


        # if [[ "$COMPOSER" > "rac" ]]
        # then
        # fi
        echo "Creating the required directories for: $COMPOSER"
        mkdir $MELODY_RNN_PATH
        mkdir $DATASET_PATH

        echo "Generating note sequences for: $COMPOSER"
        convert_dir_to_note_sequences --input_dir=$MIDI_PATH --output_file=$TFRECORD_PATH --recursive

        echo "Creating dataset for: $COMPOSER"
        melody_rnn_create_dataset --config=$CONFIG --input=$TFRECORD_PATH --output_dir=$DATASET_PATH --eval_ratio=$EVAL_RATIO

        echo "Training and evaluating the model for: $COMPOSER"
        melody_rnn_train --config=$CONFIG --run_dir=$RUN_PATH --sequence_example_file=$TRAINING_PATH --hparams=$HPARAMS --num_training_steps=$TRAINING_STEPS &
        melody_rnn_train --config=$CONFIG --run_dir=$RUN_PATH --sequence_example_file=$TRAINING_PATH --hparams=$HPARAMS --num_training_steps=$TRAINING_STEPS --eval
        melody_rnn_generate --config=$CONFIG --run_dir=$RUN_PATH --hparams=$HPARAMS --bundle_file=$BUNDLE_FILE --save_generator_bundle
    done

echo "All composers are trained successfully!"
