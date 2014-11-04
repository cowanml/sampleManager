__author__ = 'arkilic'
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
        res = None
    elif isinstance(some_object, ObjectId):
        return some_object
    else:
        raise TypeError('Entry must be a bson.ObjectId')



def validate_bool(entry):
    if isinstance(entry, bool):
        res = entry
    else:
        raise TypeError('Entry must be a boolean')
    return res

def validate_priority(entry):
    if isinstance(entry, str):
        if entry == 'High':
            return entry
        elif entry == 'Low':
            return entry
        else:
            raise ValueError('Priority can be High or Low')
    else:
        raise TypeError('Priority must be a string[High/Low]')

def validate_status(entry):
    if isinstance(entry, str):
        if entry == 'Active':
            return entry
        elif entry == 'Inactive':
            return entry
        else:
            raise ValueError('Status can be Active or Inactive')
    else:
        raise TypeError('Status must be a string[Active/Inactive]')