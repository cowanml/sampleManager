__author__ = 'arkilic'
from sampleManager.config.__conf import conf_dict


database = conf_dict.get('sampleManager', 'database')
host = conf_dict.get('sampleManager', 'host')
port = conf_dict.get('sampleManager', 'port')