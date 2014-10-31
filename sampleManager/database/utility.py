__author__ = 'arkilic'
import datetime
from bson import ObjectId


def validate_string(entry):
    if isinstance(entry, str):
        res = entry
    elif entry is None:
        res = None
    else:
        raise TypeError('Entry must be a python string')
    return res


def validate_dict(entry):
    if isinstance(entry, dict):
        res = entry
    else:
        raise TypeError('Entry must be a dictionary')
    return res


def validate_list(entry):
    if isinstance(entry, list):
        res = entry
    else:
        raise TypeError('Entry must be a list')
    return res


def validate_int(entry):
    if isinstance(entry, int):
        res = entry
    else:
        raise TypeError('Entry must be an integer')
    return res


def validate_bson_obj(some_object):
    if some_object is None:
        return None
    if isinstance(some_object, ObjectId):
        pass
    else:
        raise TypeError('Entry must be a bson.ObjectId')
