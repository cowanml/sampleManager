__author__ = 'arkilic'
from sampleManager.session.databaseInit import db
from sampleManager.database.utility import validate_list, validate_dict, validate_string, validate_int


class Container(object):
    """
    Container instance
    """
    def __init__(self, container_id, container_name, owner_group, item_list):
        """

        :param container_id: Unique identifier for a given container
        :type container_id: unspecified

        :param container_name: Name for a given container
        :type container_name:str

        :param owner_group: Identifier for given owner
        :type owner_group: int

        :param item_list:
        :type item_list: list

        :return: Container instance unique identifier
        :rtype: bson.ObjectId

        """
        #TODO: Find out which one of these fields are unique
        #TODO: Is itemlist list of all samples????
        #TODO: Which fields are required, which are optional??
        self.container_id = container_id
        self.owner_group = validate_int(owner_group)
        self.container_name = validate_string(container_name)
        self.item_list = validate_list(item_list)

    def __compose_document(self):
        document_template = dict()
        document_template['container_id'] = self.container_id
        document_template['container_name'] = self.container_name
        document_template['owner_group'] = self.owner_group
        document_template['item_list'] = self.item_list
        return document_template

    def save(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        composed_dict = self.__compose_document()
        _id = db['container'].insert(composed_dict, **kwargs)
        db['container'].ensure_index([('container_id', -1)], unique=True)
        db['container'].ensure_index([('container_name', -1), ('owner_group', -1)])
        return _id


class Sample(object):
    def __init__(self, sample_id, sample_name, collection_id, owner_group, request_list, result_list):
        """

        :param sample_id:
        :param sample_name:
        :param owner_group:
        :param request_list:
        :param result_list:
        :return:
        """
        self.sample_id = sample_id
        self.collection_id = collection_id
        self.sample_name = validate_string(sample_name)
        self.owner_group = validate_int(owner_group)
        self.request_list = validate_list(request_list)
        self.result_list = validate_list(result_list)
        #TODO: Does result list need to be updated once sample is created???
        #TODO: Updates are nasty, we shld keep it isolated if update needed How about metadataStore and/or a results
        #TODO: table with suggested fields within resultObj??

    def __compose_document(self):
        document_template = dict()
        document_template['sample_id'] = self.sample_id
        document_template['sample_name'] = self.sample_name
        document_template['owner_group'] = self.owner_group
        document_template['request_list'] = self.request_list
        document_template['result_list'] = self.result_list
        document_template['collection_id'] = self.collection_id
        return document_template

    def save(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        composed_dict = self.__compose_document()
        _id = db['sample'].insert(composed_dict, **kwargs)
        db['sample'].ensure_index([('sample_id', -1), ('collection_id', -1)], unique=True)
        db['sample'].ensure_index([('sample_name', -1), ('owner_group', -1)])
        return _id


class Request(object):
    def __init__(self, sample_id, request_dict):
        """

        :param sample_id:
        :param request_dict:
        :return:
        """
        self.sample_id = sample_id  #foreignkey
        self.request_dict = request_dict

    def __compose_document(self):
        document_template = dict()
        document_template['sample_id'] = self.sample_id
        document_template['request_dict'] = self.request_dict
        return document_template

    def save(self, **kwargs):
        composed_dict = self.__compose_document()
        _id = db['request'].insert(composed_dict, **kwargs)
        db['request'].ensure_index([('sample_id', -1)], unique=True)
        db['request'].ensure_index([('request_dict', -1)])
        return _id