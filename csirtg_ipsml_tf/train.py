#!/usr/bin/env python

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import textwrap
import pandas
import sys
from pprint import pprint

from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Embedding

from csirtg_ipsml_tf.constants import MAX_STRING_LEN, MODEL, WEIGHTS, BATCH_SIZE
from csirtg_ipsml_tf.utils import extract_features

BATCH_SIZE = int(BATCH_SIZE)
MAX_STRING_LEN = int(MAX_STRING_LEN)

NEURONS = os.getenv('NEURONS', 16)
EMBEDDED_DIM = os.getenv('EMBEDDED_DIM', 30)

NEURONS = int(NEURONS)
EMBEDDED_DIM = int(EMBEDDED_DIM)

EPOCHS = os.getenv('EPOCHS', 10)
EPOCHS = int(EPOCHS)

# training split
SPLIT = os.getenv('TRAINING_SPLIT', .3)
SPLIT = float(SPLIT)

DATA_PATH = 'data'

# https://github.com/vprusso/tf_mushroom/blob/master/tf_mushroom.py
# https://www.quora.com/How-can-TensorFlow-deep-learning-be-used-for-anomaly-detection
# https://www.quora.com/How-do-I-use-LSTM-Networks-for-time-series-anomaly-detection/answer/Pankaj-Malhotra-2
# https://jask.com/time-series-anomaly-detection-in-network-traffic-a-use-case-for-deep-neural-networks/
# http://vprusso.github.io/blog/2017/tensor-flow-categorical-data/


def train(csv_file):
    dataframe = pandas.read_csv(csv_file, engine='python', quotechar='"', header=None)
    dataset = dataframe.values

    # Preprocess dataset
    X = dataset[:, :7]
    Y = dataset[:, -1]

    train_size = int(len(dataset) * (1 - SPLIT))

    X_train, X_test = X[0:train_size], X[train_size:len(X)]
    Y_train, Y_test = Y[0:train_size], Y[train_size:len(Y)]

    model = Sequential()
    model.add(Embedding(500, EMBEDDED_DIM))
    model.add(Dropout(0.5))
    model.add(LSTM(NEURONS, recurrent_dropout=0.5))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    print(model.summary())

    model.fit(X_train, Y_train, validation_split=SPLIT, epochs=EPOCHS, batch_size=BATCH_SIZE)

    # Evaluate model
    score, acc = model.evaluate(X_test, Y_test, verbose=1, batch_size=BATCH_SIZE)

    print("Model Accuracy: {:0.2f}%".format(acc * 100))

    # Save model
    print("Saving model to: %s" % MODEL)
    model.save_weights(WEIGHTS)
    model.save(MODEL)


def main():
    p = ArgumentParser(
        description=textwrap.dedent('''\
            example usage:
                $ mkdir tmp
                $ cat data/whitelist.txt | csirtg-ipsml-tf-train --build --good > tmp/good.csv
                $ cat data/blacklist.txt | csirtg-ipsml-tf-train --build > tmp/bad.csv
                $ cat tmp/good.csv tmp/bad.csv | gshuf > data/training.csv
                $
                $ csirtg-ipsml-tf-train -f data/training.csv  # could take a few hours
            '''),
        formatter_class=RawDescriptionHelpFormatter,
    )

    p.add_argument('--good', action="store_true", default=False)
    p.add_argument('--build', action="store_true", help="Run in Build Mode (eg: build training data from "
                                                        "black/whitelists", default=False)

    p.add_argument('--training', help='path to training data [default: %(default)s]',
                   default=os.path.join('data', 'training.csv'))
    p.add_argument('-d', '--debug', dest='debug', action="store_true")

    args = p.parse_args()

    if args.build:
        for l in sys.stdin:
            l = l.rstrip()
            ts, ip = l.split(',')

            import arrow
            ts = arrow.get(ts)
            ts = ts.strftime("%Y-%m-%dT%H:%M:%SZ")

            feats = extract_features(ip, ts)
            feats = [str(e) for e in list(feats)[0]]

            if args.good:
                print('%s,0' % ','.join(feats))
            else:
                print('%s,1' % ','.join(feats))

        raise SystemExit

    print("Model location: %s" % MODEL)
    train(args.training)


if __name__ == '__main__':
    main()
