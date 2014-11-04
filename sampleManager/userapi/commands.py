__author__ = 'arkilic'
from sampleManager.dataapi.commands import save_container, save_request, save_sample, find_container
from sampleManager.dataapi.commands import find_request, find_sample
from collections import OrderedDict


def create_container(container_id, container_name, owner_group, contained_container_id=None):
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
        save_container(container_id=container_id, container_name=container_name,
                       owner_group=owner_group,contained_container_id=contained_container_id)

    except:
        raise

def add_sample(container_id, sample_id, sample_name, owner_group, sample_group_name, sample_position):
    pass


def create_request(sample_id, request_dict, request_id):
    pass


def change_sample_container():
    pass


def toggle_sample():
    pass


def toggle_request_status():
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