__author__ = 'arkilic'

from sampleManager.database.collection_definition import Container, Request, Sample
from sampleManager.session.databaseInit import db
from sampleManager.session.databaseInit import sampleManagerLogger
import bson
import pymongo
from sampleManager.database.utility import validate_status


def save_container(container_id, container_name, owner_group, capacity, container_ref_id=None, status='Active'):
    """
    :param container_id: Unique identifier for a given container
    :type container_id: unspecified

    :param container_name: Name for a given container
    :type container_name:str

    :param owner_group: Identifier for given owner
    :type owner_group: int

    :param capacity: Specifies the number of samples a container can hold
    :type capacity: int

    :return: Container instance unique identifier
    :rtype: bson.ObjectId
    """
    container_obj = Container(container_id=container_id, container_name=container_name, owner_group=owner_group,
                              container_ref_id=container_ref_id, capacity=capacity, status=status)
    try:
        cont_id = container_obj.save(wtimeout=100, write_concern={'w': 1})
    except:
        raise
    return cont_id


def save_multiple_containers(container_object_list=list()):
    """
    Provides means to bulk create set of containers given a list of container items. Likely to be deprecated.

    :param container_object_list: Given list of container objects, bulk creates containers
    :type container_object_list: list

    :return: None
    :rtype: None
    """
    if isinstance(container_object_list, list):
        temp_dict = dict()
        bulk = db['container'].initialize_ordered_bulk_op()
        if container_object_list:
            for container in container_object_list:
                if isinstance(container, Container):
                    temp_dict = container.__compose_document()
                    bulk.insert(temp_dict)
                else:
                    TypeError('Contents of container_object_list must be container objects')
            bulk.execute()
        else:
            raise IndexError('container_object_list cannot be empty')
    else:
        raise TypeError('container_object_list must be a list')


def find_container(container_query_dict):
    """
    Submits a query to container collection and returns documents that match search criteria as a pymongo.cursor object

    :param container_query_dict: Dictionary for determining

    :return: iterable container cursor
    :rtype: pymongo.Cursor
    """
    if isinstance(container_query_dict, dict):
        if container_query_dict:
            try:
                container_cursor = db['container'].find(container_query_dict)
            except:
                sampleManagerLogger.logger.warning('Cannot establish connection to container collection')
                raise
        else:
            raise ValueError('container_query_dict can not be empty')
    else:
        raise TypeError('container_query_dict must be a dictionary')
    return container_cursor


def decode_container_cursor(container_cursor):
    if isinstance(container_cursor, pymongo.cursor.Cursor):
        containers = dict()
        for temp_dict in container_cursor:
            containers[temp_dict['container_name']] = temp_dict
    else:
        raise TypeError('container cursor must be a pymongo.cursor.Cursor instance')
    return containers


def save_sample(sample_id, container_id, sample_name, owner_group, sample_group_name, sample_position):
    """
    :param sample_id: Unique identifier specific to a sample set by ABBIX collection script
    :type sample_id: int

    :param container_id: foreignkey pointing to container a sample belongs to
    :type container_id: bson.ObjectId

    :param collection_id: ???
    :type collection_id: ???

    :param sample_name: Text descriptor for sample
    :type sample_name: str

    :param owner_group: Denotes the group a specific owner belongs
    :type owner_group: int

    :param sample_group_name: provides information regarding the group sample falls under
    :type sample_group_name: str

    :param sample_position: Denotes the location of which sample is placed within a container
    :type sample_position: int

    :return: Returns _id for sample document
    :rtype: bson.ObjectId
    """
    try:
        __val_sample_pos(container_id=container_id, sample_position=sample_position)
    except:
        raise
    sample_obj = Sample(sample_id=sample_id, container_id=container_id, sample_name=sample_name,
                        owner_group=owner_group, sample_group_name=sample_group_name,
                        sample_position=sample_position)
    try:
        native_sample_id = sample_obj.save(wtimeout=100, write_concern={'w': 1})
    except:
        raise
    return native_sample_id


def find_sample(sample_query_dict=dict()):
    if isinstance(sample_query_dict, dict):
        if sample_query_dict:
            try:
                sample_cursor = db['sample'].find(sample_query_dict)
            except:
                raise
        else:
            raise ValueError('sample_query_dict cannot be empty')
    else:
        raise TypeError('sample_query_dict must be a dictionary')
    return sample_cursor


def decode_sample_cursor(sample_cursor):
    """
    Given sample cursor instance, returns a dictionary

    :param sample_cursor: Cursor object returned from queries to be decoded
    :type sample_cursor: pymongo.cursor.Cursor object

    :return: sample dictionary
    :rtype: dict
    """
    if isinstance(sample_cursor, pymongo.cursor.Cursor):
        samples = dict()
        for temp_dict in sample_cursor:
            samples[temp_dict['sample_name']] = temp_dict
    else:
        raise TypeError('sample_cursor must be a pymongo.cursor.Cursor instance')
    return samples


def get_sample_mongo_id(sample_name):
    """
    Returns unique mongodb _id given unique sample_name

    :param sample_name: Collection/User defined name for the sample
    :type sample_name: str

    :return: Sample document mongodb _id
    :rtype: bson.ObjectId
    """
    sample_obj = find_sample({'sample_name': sample_name})
    try:
        result = sample_obj[0]['_id']
    except IndexError:
        raise Exception('sample document cannot be found given sample_name ' + str(sample_name))
    try:
        temp = sample_obj[1]['_id']
        raise Exception('sample_name must be unique.')
    except IndexError:
        pass
    return result


def save_request(sample_id, request_id, request_type=None, request_dict=dict(), priority='Low'):
    """
    Creates a request entry and links it to samples provided

    :param sample_id: foreignkey pointing at a specific sample's _id field
    :type sample_id: bson.ObjectId

    :param request_dict: custom field to be filled by collection environment
    :type request_dict: dict

    :param request_type: provides information regarding nature of request
    :type request_type: str

    :return: None
    :rtype: None
    """
    request_obj = Request(sample_id, request_id, request_dict, request_type, priority)
    try:
        req_id = request_obj.save(wtimeout=100, write_concern={'w': 1})
    except:
        raise
    return req_id


def find_request(request_query_dict=dict()):
    """
    Queries request collection given request_query_dict
    :param request_query_dict:
    :return:
    """
    if isinstance(request_query_dict, dict):
        if request_query_dict:
            try:
                request_cursor = db['request'].find(request_query_dict)
            except:
                raise
        else:
            raise ValueError('request_query dict cannot be empty')
    else:
        raise TypeError('request_query_dict must be a dict')
    return request_cursor


def decode_request_cursor(request_cursor):
    """
    Parses a pymongo cursor instance from request collection and composes a python dictionary

    :param request_cursor: cursor object composed of documents that belong to request collection
    :type request_cursor: pymongo.cursor.Cursor

    :return: request document dictionary with request_id as keys
    :rtype: dict
    """
    if isinstance(request_cursor, pymongo.cursor.Cursor):
        requests = dict()
        for temp_dict in request_cursor:
            requests[temp_dict['request_id']] = temp_dict
    else:
        raise TypeError('request_cursor must be a bson.ObjectId instance')
    return requests


def get_container_mongo_id(container_name):
    """
    Returns a container _id given container name

    :param container_name: Name of the specific container
    :type container_name: str

    :return: container document _id
    :rtype: bson.ObjectId
    """
    if isinstance(container_name, str):
        cont_obj = find_container({'container_name': container_name})
    else:
        raise TypeError('container_name must be a string')
    try:
        result = cont_obj[0]['_id']
    except IndexError:
        raise Exception('container cannot be found given container_name '+ str(container_name))
    try:
        temp = cont_obj[1]['_id']
        raise Exception('container_name must be unique.')
    except IndexError:
        pass
    return result


def get_request_mongo_id(request_id):
    request_obj = find_request({'request_id': request_id})
    try:
        result =  request_obj[0]['_id']
    except IndexError:
        raise Exception('request cannot be found given request_id' + str(request_id))
    try:
        temp = request_obj[1]['_id']
        raise Exception('request_id must be unique.')
    except IndexError:
        pass
    return result


def __val_sample_pos(container_id, sample_position):
    container_query_dict = dict()
    status = False
    container_query_dict['_id'] = container_id
    try:
        cont_cursor = find_container(container_query_dict=container_query_dict)
    except:
        sampleManagerLogger.logger.warning('Container cursor could not be parsed')
        raise
    capacity = cont_cursor[0]['capacity']
    sample_query_dict = dict()
    sample_query_dict['container_id'] = bson.ObjectId(container_id)
    samples = find_sample(sample_query_dict=sample_query_dict)
    if sample_position > capacity:
            status = False
            raise ValueError('Sample position cannot be larger than the container capacity')
    else:
        for sample in samples:
            if sample_position == sample['sample_position']: #or (sample_position > capacity):
                status = False
                raise ValueError('Two samples cannot be on the same spot')
                break
            else:
                status = True
    return status


def validate_sample_position(container_name, sample_position ):
    container_query_dict = dict()
    container_query_dict['container_name'] = container_name
    try:
        cont_cursor = find_container(container_query_dict=container_query_dict)
    except:
        sampleManagerLogger.logger.warning('Container cursor could not be parsed')
        raise
    container_dict = decode_container_cursor(cont_cursor)
    container = container_dict[container_name]
    capacity = container['capacity']
    container_id = container['_id']
    sample_query_dict = dict()
    # sample_query_dict['container_id'] = bson.ObjectId(container_id)
    sample_query_dict['container_id'] = container_id
    samples = find_sample(sample_query_dict=sample_query_dict)
    for sample in samples:
        if sample_position > capacity:
            raise ValueError('Sample position cannot be larger than the container capacity')
            break
        if sample_position == sample['sample_position']: #or (sample_position > capacity):
            raise ValueError('Sample Position is invalid')
            break

    validate_flag = True
    return validate_flag


def update_container_status(container_id, status):
    validate_status(status)
    container = db['container'].find_one({"container_id": container_id})
    container['status'] = status
    try:
        db['container'].save(container)
    except:
        raise Exception('Container status cannot be updated')
