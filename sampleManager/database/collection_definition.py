__author__ = 'arkilic'
from sampleManager.session.databaseInit import db
from sampleManager.database.utility import validate_list, validate_dict, validate_string, validate_int
from sampleManager.database.utility import validate_container_ref_ids


class Container(object):
    """
    Container instance
    """
    def __init__(self, container_id, container_name, owner_group, container_ref_id, capacity):
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
        #TODO: Find out which one of these fields are unique
        #TODO: Which fields are required, which are optional??
        #TODO: Add validate container_ref_id routine [it is a list of bson.ObjectId objects]
        self.container_id = container_id
        self.owner_group = validate_int(owner_group)
        self.container_name = validate_string(container_name)
        self.container_ref_id = validate_list(container_ref_id)
        self.capacity = validate_int(capacity)

    def __compose_document(self):
        """
        pymongo document entry composer. Given fields within a class, returns a python dictionary to be converted to
        bson object by pymongo

        :return: Container document dictionary
        :rtype: dict
        """
        document_template = dict()
        document_template['container_id'] = self.container_id
        document_template['container_name'] = self.container_name
        document_template['owner_group'] = self.owner_group
        document_template['container_ref_id'] = self.container_ref_id
        document_template['capacity'] = self.capacity

        return document_template

    def save(self, **kwargs):
        """
        :param kwargs: pymongo driver specific instructions regarding insert operation
        :type kwargs: dict

        :return: Container document _id field
        :rtype: bson.ObjectId
        """
        composed_dict = self.__compose_document()
        _id = db['container'].insert(composed_dict, **kwargs)
        db['container'].ensure_index([('container_id', -1)], unique=True)
        db['container'].ensure_index([('container_name', -1)], unique=True)
        return _id


class Sample(object):
    def __init__(self, sample_id, container_id, sample_name, owner_group, sample_group_name, sample_position):
        """
        Sample object constructor

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


        :return: None
        :rtype: None
        """
        #TODO: Find out which one of these fields are unique
        #TODO: Which fields are required, which are optional??
        self.sample_id = sample_id
        self.container_id = container_id
        self.sample_name = validate_string(sample_name)
        self.owner_group = validate_int(owner_group)
        self.sample_group_name = validate_string(sample_group_name)
        self.sample_position = validate_int(sample_position)

    def __compose_document(self):
        """
        pymongo document entry composer. Given fields within a class, returns a python dictionary to be converted to
        bson object by pymongo

        :return: sample document dictionary
        :rtype: dict
        """

        document_template = dict()
        document_template['sample_id'] = self.sample_id
        document_template['sample_name'] = self.sample_name
        document_template['owner_group'] = self.owner_group
        document_template['container_id'] = self.container_id
        document_template['sample_group_name'] = self.sample_group_name
        document_template['sample_position'] = self.sample_position
        return document_template

    def save(self, **kwargs):
        """
        Insert a document into Sample collection using the template mandated by the Sample class constructor

        :param kwargs: pymongo driver specific instructions regarding insert operation
        :type kwargs: dict

        :return: Sample document _id field
        :rtype: bson.ObjectId
        """
        composed_dict = self.__compose_document()
        _id = db['sample'].insert(composed_dict, **kwargs)
        db['sample'].ensure_index([('sample_id', -1)], unique=True)
        db['sample'].ensure_index([('container_id', -1)])
        db['sample'].ensure_index([('sample_name', -1)], unique=True)
        db['sample'].ensure_index([('owner_group', -1)])
        db['sample'].ensure_index([('sample_position', -1)])
        return _id


class Request(object):
    def __init__(self, sample_id, request_id, request_dict, request_type):
        """

        :param sample_id: foreginkey pointing at a specific sample's _id field
        :type sample_id: bson.ObjectId

        :param request_dict: custom field to be filled by ABBOX collection environment
        :type request_dict: dict

        :param request_type: provides information regarding nature of request
        :type request_type: str

        :return: None
        :rtype: None
        """
        self.sample_id = sample_id
        self.request_dict = request_dict
        self.request_id = request_id
        self.request_type = request_type

    def __compose_document(self):
        """
        pymongo document entry composer. Given fields within a class, returns a python dictionary to be converted to
        bson object by pymongo

        :return: Request document dictionary
        :rtype: dict
        """
        document_template = dict()
        document_template['sample_id'] = self.sample_id
        document_template['request_dict'] = self.request_dict
        document_template['request_id'] = self.request_id
        document_template['request_type'] = self.request_type
        return document_template

    def save(self, **kwargs):
        """
        Insert a document into Sample collection using the template mandated by the Request class constructor

        :param kwargs: pymongo driver specific instructions regarding insert operation

        :return: Request document _id field
        :rtype: bson.ObjectId
        """
        composed_dict = self.__compose_document()
        _id = db['request'].insert(composed_dict, **kwargs)
        db['request'].ensure_index([('sample_id', -1)], unique=True)
        db['request'].ensure_index([('request_id', -1)], unique=True)
        db['request'].ensure_index([('request_type', -1)])
        db['request'].ensure_index([('request_dict', -1)])
        return _id