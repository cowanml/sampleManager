from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import six
import datetime
import logging
import uuid
from functools import wraps
from mongoengine import connect

#from metadatastore.document import Document
#from metadatastore.commands import (db_connect, db_disconnect, _ensure_connection,
#                                    _normalize_object_id, _format_time)

from . import conf


from .util import (new_uid, get_owner)
from .odm_templates import (Sample, SampleGroup, Container, Request, SMType)


logger = logging.getLogger(__name__)


# Data insertion/modification

def insert_sample(uid=None, owner=None, type=None, properties=None, name=None, identifier=None, container=None, position=None, custom=None):
    """
    Insert a new sample

    Parameters
    ----------
    uid, owner, type, and properties

    name : str
        A short, human readable, name for the sample.

    identifier : str
        An identifier for the sample.  Meant for machine
        readable stuff:  serial#, barcode, etc.

    name and identifier are optional, but atleast one is required.

    container : samplemanager.odm_templates.Container, optional?
        Foreign key to container holding the sample.

    position : str, optional?
        Position within the container

    custom : dict, optional
        Any additional information to attach to the sample.

    Returns
    -------
    sample: mongoengine.Document
        Inserted mongoengine object
    """

    # default uid creation inherited from SMDynDoc

    if owner is None:
        raise ValueError('Must specify owner.')

    if type is None:
        raise ValueError('Must specify type.')

    if name is None and identifier is None:
        raise ValueError('Must specify atleast one of "name" or "identifier".')

    sample = Sample(uid=uid, owner=owner, type=type, properties=properties,
                    name=name, identifier=identifier, container=container, position=position,
                    **custom)

    sample.save(validate=True, write_concert={"w": 1})
    logger.debug('Inserted Sample with uid %s', sample.uid)

    return sample


def insert_sample_group(uid=None, owner=None, type=None, properties=None, name=None, custom=None):
    """
    Holds info about related groups of samples.

    eg. For measurements requiring multiple samples to complete,
    like tiny crystals which are destroyed before a full dataset
    can be collected... need lots of the tiny crystals, and this data
    structure to store overall completeness information, etc.

    Parameters
    ----------
    uid, owner, type, and properties

    name : str
       A short, human readable, name for the sample group.
    
    """

    # default uid creation inherited from SMDynDoc    

    if uid == None:
        uid = str(new_uid('sample_group'))

    sample_group = SampleGroup(uid=uid, owner=owner, type=type, properties=properties,
                     name=name, **custom)

    sample_group.save(validate=True, write_concert={"w": 1})
    logger.debug('Inserted Sample Group with uid %s', sample_group.uid)

    return sample_group
    


def insert_container(uid=None, owner=None, type=None, properties=None,
                     ):
    """
    """

def insert_request():
    """
    """


def insert_type(uid=None, owner=None, type=None, properties=None,
                name=None):
    """
    Create a new type (sample, container, request, whatever)

    Parameters
    ----------
    uid, owner, and properties inherited from SMDynDoc  

    name : str
        The name of the new type.

    Returns
    -------
    sm_type: mongoengine.Document
        Inserted mongoengine object
    """

    # default uid creation inherited from SMDynDoc

    if owner is None:
        raise ValueError('Must specify owner.')

    if name is None:
        raise ValueError('Must specify name.')

    sm_type = SMType(uid=uid, owner=owner, type=type, properties=properties,
                     name=name)

    sm_type.save(validate=True, write_concert={"w": 1})
    logger.debug('Inserted SMType with uid %s', sm_type.uid)

    return sm_type
    

def insert_sample_type():
    """
    """

def insert_container_type():
    """
    """

def insert_request_type():
    """
    """


# Data retrieval 

def find_samples(**kwargs):
    """
    """

def find_sample_groups(**kwargs):
    """
    """

def find_containers(**kwargs):
    """
    """

def find_requests(**kwargs):
    """
    """


def find_types(**kwargs):
    """
    """

def find_sample_types(**kwargs):
    """
    """

def find_container_types(**kwargs):
    """
    """

def find_request_types(**kwargs):
    """
    """


#from .commands import (change_request_priority, change_sample_container)
#from .commands import (toggle_sample, update_container_status)

# __val_sample_pos, _isinstance, decode_{container,request,sample}_cursor
# get_{container,request,sample}_mongo_id
# save_multiple_containers

# maybe? insert_{samples,containers,requests}
# update_{location,status,priority,request}
# rename(obj_type, obj, new_name)
# or generic update could provide for rename?
# delete_[obj[s]]

# ?
# insert_{type,class}
# save_{type,class}
# insert_{types,classes}

# get_all
# get_by_{id,type}
# get_special_by_name (getPrimaryDewar)
# get_{contents,grouping,requests}_by_id
#   drop the the _by_id's?
# get_queue
