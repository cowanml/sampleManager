__author__ = 'arkilic'
from sampleManager.dataapi.commands import save_container, save_request, save_sample, find_container
from sampleManager.dataapi.commands import find_request, find_sample

try:
    from collections import OrderedDict
except ImportError:
    # for < 2.7
    from ordereddict import OrderedDict

from pymongo import errors
from sampleManager.session.databaseInit import sampleManagerLogger


def create_container(container_id, container_name, owner_group, capacity=10, contained_container_id=None, status='Active'):
    """
    Creates a container given information.

    :param container_id: User/Collection script defined unique identifier
    :type container_id:int, str, bson.ObjectId

    :param container_name: User/Collection script defined unique string
     :type container_name: str

    :param owner_group: Container owner information
    :type owner_group: str

    :param contained_container_id: Indicates within which container the container to be created is encapsulated
    :type contained_container_id: bson.ObjectId

    :return: None
    :rtype: None
    """
    try:
        res = save_container(container_id=container_id, container_name=container_name, owner_group=owner_group,
                       capacity=capacity, container_ref_id=contained_container_id, status=status)
    except:
        raise
    return res


def add_sample(container_id, sample_id, sample_name, owner_group, sample_group_name, sample_position=1):
    """
    Adds a sample to database within a given container

    :param sample_id: Unique identifier specific to a sample set by collection script
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
        res = save_sample(sample_id=sample_id, container_id=container_id, sample_name=sample_name, owner_group=owner_group,
                    sample_group_name=sample_group_name, sample_position=sample_position)
    except:
        raise pymongo.error
    return res


def create_request(sample_id, request_id, request_dict={}, request_type=None, priority='Low'):
    """
    Creates a request entry and links it to samples provided

    :param request_id: Unique identifier denoting a request
    :type request_id:int, str, bson.ObjectId

    :param sample_id: foreignkey pointing at a specific sample's _id field
    :type sample_id: bson.ObjectId

    :param request_dict: custom field to be filled by collection environment
    :type request_dict: dict

    :param request_type: provides information regarding nature of request
    :type request_type: str

    :return: None
    :rtype: None
    """
    try:
        req_id = save_request(sample_id=sample_id, request_id=request_id, request_type=request_type,
                     request_dict=request_dict, priority=priority)
    except:
        sampleManagerLogger.logger.warning('Request cannot be created')
        raise errors.ConnectionFailure('Request cannot be created')
    return req_id


def change_sample_container(sample_name, container_id):
    """
    Moves sample from one container to another given sample_name and new container_id

    :param sample_name: name of the sample to be moved to a different container
    :type sample_name: str

    :param container_id: User/Collection script defined unique identifier for the new container
    :type container_id: int, str, bson.ObjectId

    :return: None
    """
    #TODO: Check if sample exists
    #TODO: Check if container exists
    #TODO: Validate sample position given container
    #TODO: Update sample position if above criteria satisfied
    pass


def toggle_sample(sample_name, state):
    """
    Sets the state of the sample[Active/Inactive]

    :param sample_name: name of the sample to be set/reset
    :type sample_name: str

    :param state: True is sample is Active and False if sample is Inactive
    :type state: bool

    :return: None
    """
    #TODO: Check if sample exists
    #TODO: Check if the state is different than existing state
    #TODO: If state is different, change the sample state
    pass


def change_request_priority(request_id, priority):
    """
    Changes the priority of a request. There are two priority levels: High/Low

    :param request_id: id of the request that will be assigned a new priority.
    :type request_id:

    :param priority:
    :return:
    """


    pass


def find():
    pass


def _isinstance(inquired_value, target_type):
    if isinstance(inquired_value, target_type):
        return inquired_value
    else:
        value = target_type(inquired_value)
        if isinstance(value, target_type):
            return value
        else:
            raise TypeError()


container_keys = OrderedDict()
container_keys['container_id'] = {'description': "The unique identifier for a container",
                                  'type': int,
                                  'validate_fun': _isinstance}

container_keys['container_name'] = {'description': "The unique name for a container",
                                    'type': str,
                                    'validate_fun': _isinstance}

container_keys['owner_group'] = {'description': 'Specifies the group container owner',
                                 'type': int,
                                 'validate_fun': _isinstance}

container_keys['contained_container_id'] = {'description': 'Reference to containers encapsulated within ',
                                            'type': int,
                                            'validate_fun': _isinstance}

sample_keys = OrderedDict()

sample_keys['sample_id'] = {'description': 'The unique identifier for a sample',
                            'type': int,
                            'validate_fun': _isinstance}

sample_keys['container_id'] = {'description': "The unique identifier for a container",
                               'type': int,
                               'validate_fun': _isinstance}

sample_keys['sample_name'] = {'description': "The unique name of the sample",
                              'type': str,
                              'validate_fun': _isinstance}

sample_keys['owner_group'] = {'description': 'Specifies the group container owner',
                              'type': int,
                              'validate_fun': _isinstance}
request_keys = OrderedDict()

request_keys['sample_id'] = {'description': 'The unique identifier for a sample',
                            'type': int,
                            'validate_fun': _isinstance}

request_keys['request_id'] = {'description': "The unique identifier for a request",
                              'type': int,
                              'validate_fun': _isinstance}

request_keys['request_dict'] = {'description': "Name-value container containing steps/tasks for the given request",
                                'type': dict,
                                'validate_fun': _isinstance}
