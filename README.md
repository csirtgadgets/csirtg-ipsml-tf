# csirtg-ipsml-tf
simple library for detecting suspicious connections using TensorFlow

This model is very simple and looks at features such as:

* Time of day (hour)
* General Long / Lat
* TimeZone
* Country Code
* ASN

NOTE: THE DEFAULT DATA-SETS ARE NOT STATISTICALLY SOUND

While not meant to be perfect, meant to demonstrate how you might look at suspicious connections and build a VERY SIMPLE machine learning model around those features.

https://github.com/csirtgadgets/csirtg-ipsml-py (SKLearn based Only)
https://csirtgadgets.com/commits/2018/4/20/predicting-attacks-with-python-and-sklearn
https://csirtgadgets.com/commits/2018/3/8/hunting-for-suspicious-domains-using-python-and-sklearn
https://csirtgadgets.com/commits/2018/3/30/hunting-for-threats-like-a-quant

```bash
$ sudo [apt-get|brew|yum] install geoipupdate  # ubuntu16 or later, should use if you can python3
$ sudo geoipupdate -v
$ pip install -r dev_requirements.txt
$ python setup.py develop
$ bash helpers/build.sh

$ csirtg-ipsml-tf -i 122.2.223.242,6  # indicator, hour-detected
0.50 - 122.2.223.242,6 # 50% probabiltiy

$ csirtg-ipsml-tf -i 141.142.164.33  # indicator, hour-detected
0.31 - 141.142.164.33 # 31% probability
```

# COPYRIGHT AND LICENSE

Copyright (C) 2018 [the CSIRT Gadgets](http://csirtgadgets.com)

Free use of this software is granted under the terms of the [Mozilla Public License (MPLv2)](https://www.mozilla.org/en-US/MPL/2.0/).