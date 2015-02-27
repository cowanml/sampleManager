__author__ = 'arkilic'

import glob
from os.path import basename
from os.path import splitext

from distutils.core import setup
from setuptools import find_packages

setup(
    name='sampleManager',
    version='0.0.x',
    author='Arman Arkilic',
    author_email='None',
    url='https://github.com/cowanml/sampleManager.git',
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(i))[0] for i in glob.glob("src/*.py")],
    install_requires=[
        "pymongo",
        #"mongoengine"
    ],
    )
