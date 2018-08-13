#!/usr/bin/env python

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import sys, gc
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import textwrap

from keras import backend as K
from keras.models import load_model

from csirtg_ipsml_tf.constants import MODEL, WEIGHTS, MAX_STRING_LEN, WORD_DICT
from csirtg_ipsml_tf.utils import extract_features, normalize_ips


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
                    $ csirtg-ipsml-tf -i 18.210.110.64,34.235.98.66
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

    # indicators = [urlparse(i.lower()).geturl() for i in indicators]
    indicators = normalize_ips(indicators)

    predictions = predict(indicators)

    for idx, v in enumerate(indicators):
        print("%f - %s" % (predictions[idx], v))


if __name__ == '__main__':
    main()

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
