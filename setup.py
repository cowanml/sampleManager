__author__ = 'arkilic'

from distutils.core import setup

setup(
    name='sampleManager',
    version='0.0.x',
    author='Arman Arkilic',
    packages=["sampleManager",
              "sampleManager.collectionapi",
              "sampleManager.config",
              "sampleManager.dataapi",
              "sampleManager.database",
              "sampleManager.session",
              "sampleManager.userapi",
              ],
    )
