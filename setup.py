import os
from setuptools import setup, find_packages
import versioneer
import sys


# https://www.pydanny.com/python-dot-py-tricks.html
if sys.argv[-1] == 'test':
    test_requirements = [
        'pytest',
        'coverage',
        'pytest_cov',
    ]
    try:
        modules = map(__import__, test_requirements)
    except ImportError as e:
        err_msg = e.message.replace("No module named ", "")
        msg = "%s is not installed. Install your test requirements." % err_msg
        raise ImportError(msg)
    r = os.system('py.test test -v --cov=csirtg_ipsml_tf --cov-fail-under=40')
    if r == 0:
        sys.exit()
    else:
        raise RuntimeError('tests failed')


data_files = [
    'data/model.h5',
    'data/weights.h5',
    'data/cc.txt',
    'data/timezones.txt'
]

setup(
    name="csirtg_ipsml_tf",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="CSIRTG IP ML Framework - TensorFlow",
    long_description="",
    url="https://github.com/csirtgadgets/csirtg-ipsml-tf-py",
    license='MPLv2',
    data_files=[(os.path.join('csirtg_ipsml_tf', 'data'), data_files)],
    keywords=['network', 'security'],
    author="Wes Young",
    author_email="wes@csirtgadgets.com",
    packages=find_packages(),
    install_requires=[
        'tensorflow==1.8',
        'pandas',
        'keras',
        'ipaddress',
        'scipy',
        'scikit-learn',
        'numpy',
        'geoip2',
        'arrow',
        'maxminddb',
    ],
    entry_points={
       'console_scripts': [
           'csirtg-ipsml-tf-train=csirtg_ipsml_tf.train:main',
           'csirtg-ipsml-tf=csirtg_ipsml_tf:main'
       ]
    },
)
