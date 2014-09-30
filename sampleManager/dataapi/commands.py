__author__ = 'arkilic'

from sampleManager.session.databaseInit import return_db
from sampleManager.database.collection_definition import Container, Request, Sample


def save_container(container_id, container_name, owner_group, item_list=list()):
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
    container_obj = Container(container_id=container_id, container_name=container_name, owner_group=owner_group,
                              item_list=item_list)
    try:
        container_obj.save()
    except:
        raise

