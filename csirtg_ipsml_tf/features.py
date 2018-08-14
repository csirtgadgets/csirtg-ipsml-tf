import os, sys
from csirtg_ipsml_tf.constants import PYVERSION
from sklearn import preprocessing

me = os.path.dirname(__file__)
CC_FILE = "%s/../data/cc.txt" % me

if os.path.exists(os.path.join(sys.prefix, 'csirtg_ipsml_tf', 'data', 'cc.txt')):
    CC_FILE = os.path.join(sys.prefix, 'csirtg_ipsml_tf', 'data', 'cc.txt')

elif os.path.exists(os.path.join('/usr', 'local', 'csirtg_ipsml_tf', 'data', 'cc.txt')):
    CC_FILE = os.path.join('/usr', 'local', 'csirtg_ipsml_tf', 'data', 'cc.txt')

elif os.path.exists(("%s/data/cc.txt" % me)):
    CC_FILE = "%s/data/cc.txt" % me

CC = []

TZ_FILE = "%s/../data/timezones.txt" % me

if os.path.exists(os.path.join(sys.prefix, 'csirtg_ipsml_tf', 'data', 'timezones.txt')):
    TZ_FILE = os.path.join(sys.prefix, 'csirtg_ipsml_tf', 'data', 'timezones.txt')

elif os.path.exists(os.path.join('/usr', 'local', 'csirtg_ipsml_tf', 'data', 'timezones.txt')):
    TZ_FILE = os.path.join('/usr', 'local', 'csirtg_ipsml_tf', 'data', 'timezones.txt')

elif os.path.exists(("%s/data/timezones.txt" % me)):
    TZ_FILE = "%s/data/timezones.txt" % me

TZ = []

if PYVERSION == 2:
    with open(CC_FILE) as F:
        for l in F.readlines():
            l = l.strip("\n")
            l = l.split(";")
            CC.append(l[1])
else:
    with open(CC_FILE, encoding='utf-8', errors='ignore') as F:
        for l in F.readlines():
            l = l.strip("\n")
            l = l.split(";")
            CC.append(l[1])

with open(TZ_FILE) as F:
    for l in F.readlines():
        TZ.append(l.rstrip("\n"))

cc_data = preprocessing.LabelEncoder()
cc_data.fit(CC)

tz_data = preprocessing.LabelEncoder()
tz_data.fit(TZ)
