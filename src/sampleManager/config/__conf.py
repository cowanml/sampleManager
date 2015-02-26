__author__ = 'arkilic'

import os.path
import ConfigParser
from os import path


config_path = [os.path.join(*d) for d in (
        (os.path.expanduser('~'), '.config', 'samplemanager', 'connection.conf'),
        (os.path.expanduser('~'), '.samplemanager.conf'),
        ('/etc', 'samplemanager', 'connection.conf'),
        ('.', 'samplemanager.conf')
        )]


def check_config_file():
    result = False

    for f in config_path:
        if path.isfile(f):
            result = True

    return result


def __loadConfig():
    cf=ConfigParser.SafeConfigParser()

    if check_config_file():
        cf.read(config_path)
    else:
        raise IOError('sampleManager configuration file does not exist')

    return cf


conf_dict = __loadConfig()
