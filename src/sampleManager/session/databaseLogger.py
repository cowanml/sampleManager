__author__ = 'arkilic'

import logging


class DbLogger(object):
    def __init__(self, db_name, host, port):
        """
        Constructor: MongoClient, Database, and native python loggers are created
        """
        self.logger = logging.getLogger('sampleManager')
        log_handler = logging.FileHandler('/var/tmp/sampleManager.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        log_handler.setFormatter(formatter)
        self.logger.addHandler(log_handler)
        self.logger.setLevel(logging.WARNING)
        self.host = host
        self.port = port
        self.db_name = db_name