#!/usr/bin/env python

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import sys, gc
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import textwrap
from pprint import pprint
import arrow

from keras import backend as K
from keras.models import load_model

from csirtg_ipsml_tf.constants import MODEL, WEIGHTS, MAX_STRING_LEN, WORD_DICT
from csirtg_ipsml_tf.utils import extract_features, normalize_ips
from csirtg_ipsml_tf.features import tz_data, cc_data


def predict(i):
    model = load_model(MODEL)
    model.load_weights(WEIGHTS)
    p = model.predict(i)

    K.clear_session()
    gc.collect()

    return p


def main():
    p = ArgumentParser(
        description=textwrap.dedent('''\
                example usage:
                    $ csirtg-ipsml-tf -i 18.210.110.64,17|34.235.98.66,04
                '''),
        formatter_class=RawDescriptionHelpFormatter,
    )

    p.add_argument('-i', '--indicators', help='indicator(s), pipe delimited')
    p.add_argument('-d', '--debug', dest='debug', action="store_true")

    args = p.parse_args()

    if not sys.stdin.isatty():
        indicators = sys.stdin.read().split("\n")
        indicators = indicators[:-1]
    else:
        indicators = args.indicators.split('|')

    indicators_new = []
    for l in indicators:
        if ',' not in l:
            ip = l
            ts = arrow.utcnow().hour
        else:
            ip, ts = l.split(',')

        f = list(extract_features(ip, ts))
        indicators_new.append(f[0])

    predictions = predict([indicators_new])

    for idx, v in enumerate(indicators):
        print('%.2f - %s' % (predictions[idx], v))


if __name__ == '__main__':
    main()
