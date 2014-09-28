__author__ = 'arkilic'

import os.path
import ConfigParser
from os import path


def check_config_file():
    result = False
    if path.isfile('/etc/sampleManager.conf'):
        result = True
    if path.isfile(os.path.expanduser('~/sampleManager.conf')):
        result = True
    if path.isfile('sampleManager.conf'):
        result = True
    return result


def __loadConfig():
    cf=ConfigParser.SafeConfigParser()
    if check_config_file():
        cf.read([
            '/etc/sampleManager.conf',
            os.path.expanduser('~/sampleManager.conf'),
            'dataBroker.conf'
        ])
    else:
        raise IOError('sampleManager configuration file does not exist')
    return cf


conf_dict = __loadConfig()