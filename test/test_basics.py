# -*- coding: utf-8 -*-
from csirtg_ipsml_tf import predict
from faker import Faker
from random import sample
from pprint import pprint
from time import time
import os, random
import re
import arrow
from csirtg_ipsml_tf.utils import extract_features

fake = Faker()


IPS = [
    ['141.142.234.238', 0],
    ['128.205.1.1', 1],
    ['128.205.1.1', 17]
]

THRESHOLD = 0.92
SAMPLE = int(os.getenv('CSIRTG_IPSML_TEST_SAMPLE', 200))


def _stats(u, inverse=False):
    n = 0
    positives = 0
    t1 = time()

    pprint(u)
    f = []
    for p in u:
        feats = list(extract_features(p[0], p[1]))
        pprint(feats)
        f.append(feats[0])

    p = predict([f])

    #pprint(p)

    for idx, v in enumerate(f):
        if p[idx] >= 0.68:
            positives += 1
        n += 1

    t2 = time()
    total = t2 - t1
    per_sec = SAMPLE / total
    print("seconds: %.2f" % total)
    print("rate: %.2f" % per_sec)

    n = (float(positives) / n)
    print(n)
    return n


def test_feats():
    feats = list(extract_features('141.142.234.238', 0))
    assert feats
    #assert feats == [[0, 130, 92, 88, 233]], 'did you install the maxmind geo data?'


def test_basics():
    n = _stats(IPS)
    assert n < 0.32


def test_random():
    s = []
    for d in range(0, SAMPLE):
        s.append([str(fake.ipv4()), random.randint(0, 23)])

    n = _stats(s)
    assert .16 < n < .84


def test_network():
    i = str('42.0.32.0/19')

    feats = list(extract_features(i, 22))

    p = predict([feats])

    assert p[0][0] >= 0.84

# def test_blacklist():
#     d = []
#     with open('data/blacklist.txt') as FILE:
#         for l in FILE.readlines():
#             l = l.rstrip("\n")
#             l = re.sub(r'\r|"', '', l)
#             l = l.split(',')
#             l[0] = arrow.get(l[0]).hour
#             d.append(l)
#
#     d = sample(d, SAMPLE)
#
#     n = _stats(d)
#     assert n > THRESHOLD


# def test_whitelist():
#     d = []
#     with open('data/whitelist.txt') as FILE:
#         for l in FILE.readlines():
#             l = l.rstrip("\n")
#             l = re.sub(r'\r|"', '', l)
#             l = l.split(',')
#             l[0] = arrow.get(l[0]).hour
#             d.append(l)
#
#     d = sample(d, 15)
#     n = _stats(d, inverse=True)
#     assert n > THRESHOLD
