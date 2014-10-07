__author__ = 'arkilic'

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from sampleManager.config.parseConfig import database, host, port
from sampleManager.session.databaseLogger import DbLogger


try:
    conn = MongoClient(host=host, port=int(port))
    db = conn['sampleManager']
except:
    raise ConnectionFailure('Connection cannot be established')

metadataLogger = DbLogger(db_name=database, host=host, port=int(port))