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

if __package__ is None:
    import conf

    from util import (new_uid, get_owner)
    from odm_templates import (Sample, Location, Request, SMType)

else:
    from . import conf
    
    from .util import (new_uid, get_owner)
    from .odm_templates import (Sample, Location, Request, SMType)


logger = logging.getLogger(__name__)


# Data insertion/modification

def insert_sample(uid=None, owner=None, type=None, prop=None,
                  name=None, identifier=None,
                  location=None, position=None,
                  custom=None):
    """
    Insert a new sample

    Parameters
    ----------
    uid, owner, type, and prop : inherited from SMPhysicalObj

    name : str, optional
        A short, human readable, name for the sample.

    identifier : str
        An identifier for the sample.  Meant for machine
        readable stuff:  serial#, barcode, etc.

    Name and identifier are optional, but atleast one is required,
    and name will be copied to identifier if only name is given.

    location : samplemanager.odm_templates.Location,
        Foreign key to location holding the sample.
    position : str, optional
        Position within the location/container

    custom : dict, optional
        Any additional information to attach to the sample.
        Dictionary is unpacked, and elements attached directly to
        sample.  To attach a dictionary it must be nested inside
        custom.

    Returns
    -------
    sample: mongoengine.Document
        Inserted mongoengine object
    """

    sample = Sample(uid=uid, owner=owner, type=type, prop=prop,
                    name=name, identifier=identifier,
                    location=location, position=position,
                    **custom)

    sample.save(validate=True, write_concert={"w": 1})
    logger.debug('Inserted Sample with uid %s', sample.uid)

    return sample


# not quite fully baked...
#def insert_sample_group(uid=None, owner=None, type=None, prop=None,
#                        name=None, custom=None):
#    """
#    Holds info about related groups of samples.
#
#    eg. For measurements requiring multiple samples to complete,
#    like tiny crystals which are destroyed before a full dataset
#    can be collected... need lots of the tiny crystals, and this data
#    structure to store overall completeness information, etc.
#
#    Parameters
#    ----------
#    uid, owner, type, and prop : inherited from SMDynDoc
#
#    name : str
#       A short, human readable, name for the sample group.
#    
#    """
#
#    sample_group = SampleGroup(uid=uid, owner=owner, type=type, prop=prop,
#                     name=name, **custom)
#
#    sample_group.save(validate=True, write_concert={"w": 1})
#    logger.debug('Inserted Sample Group with uid %s', sample_group.uid)
#
#    return sample_group
    


def insert_location(uid=None, owner=None, type=None, prop=None,
                     name=None, identifier=None,
                     location=None, position=None,
                     custom=None):
    """
    Insert a new location

    Parameters
    ----------
    uid, owner, type, and prop : inherited from SMPhysicalObj

    name : str, optional
        A short, human readable, name for the location.

    identifier : str
        An identifier for the location.  Meant for machine
        readable stuff:  serial#, barcode, etc.

    Name and identifier are optional, but atleast one is required,
    and name will be copied to identifier if only name is given.

    location : samplemanager.odm_templates.Location, ~optional
        Foreign key to a location/container containing this location/container.
    position : str, ~optional
        Position within the location/container

    custom : dict, optional
        Any additional information to attach to the location.
        Dictionary is unpacked, and elements attached directly to
        location.  To attach a dictionary it must be nested inside
        custom.

    Returns
    -------
    location: mongoengine.Document
        Inserted mongoengine object
    """
    
    location = Location(uid=uid, owner=owner, type=type, prop=prop,
                          name=name, identifier=identifier,
                          location=location, position=position,
                          **custom)

    location.save(validate=True, write_concert={"w": 1})
    logger.debug('Inserted Location with uid %s', location.uid)

    return location


def insert_request(uid=None, owner=None, type=None, prop=None,
                   custom=None):
    """
    Insert a new request

    Parameters
    ----------
    uid, owner, type, and prop : inherited from SMDynDoc

    custom : dict, optional
        Any additional information to attach to the request.
        Dictionary is unpacked, and elements attached directly to
        request.  To attach a dictionary it must be nested inside
        custom.

    Returns
    -------
    request: mongoengine.Document
        Inserted mongoengine object
    """

    request = Request(uid=uid, owner=owner, type=type, prop=prop,
                          **custom)

    request.save(validate=True, write_concert={"w": 1})
    logger.debug('Inserted Request with uid %s', request.uid)

    return request

# a way to make reusable requests?
#def insert_named_request():


def _insert_type(uid=None, owner=None, type=None, prop=None,
                 name=None,
                 prop_keys=None,
                 custom=None):
    """
    Create a new type (sample, location, request, whatever)

    Parameters
    ----------
    uid, owner, type, and prop : inherited from SMDynDoc

    type is optional
    prop is optional

    name : str
        The name of the new type.

    prop_keys : dict, optional
        Dict of TypeKey dicts of properties (prop) for objects of this type.

        { 'property_name1':
          { desc: str,  # description
            dtype: [integer|number|array|boolean|string],  # datatype
            validator: str,  # name of validator function
            default: str  # default value
          }, ...}

    custom : dict, optional
        Any additional information to attach to the request.
        Dictionary is unpacked, and elements attached directly to
        request.  To attach a dictionary it must be nested inside
        custom.

    Returns
    -------
    sm_type: mongoengine.Document
        Inserted mongoengine object
    """

    # default uid creation inherited from SMDynDoc

    sm_type = SMType(uid=uid, owner=owner, type=type, prop=prop,
                     name=name,
                     prop_keys=prop_keys,
                     **custom)

    sm_type.save(validate=True, write_concert={"w": 1})
    logger.debug('Inserted SMType with uid %s', sm_type.uid)

    return sm_type
    

def insert_sample_type(uid=None, owner=None, prop=None,
                       name=None,
                       prop_keys=None,
                       custom=None):
    """
    """

    type = find_types()

    _insert_type(uid=uid, owner=owner, type=type, prop=prop,
                 name=name,
                 **custom)

def insert_location_type(uid=None, owner=None, prop=None,
                       name=None,
                       prop_keys=None,
                       custom=None):
    """
    """

    type = find_types()

    _insert_type(uid=uid, owner=owner, type=type, prop=prop,
                 name=name,
                 **custom)

def insert_request_type(uid=None, owner=None, prop=None,
                       name=None,
                       prop_keys=None,
                       custom=None):
    """
    """

    type = find_types()

    _insert_type(uid=uid, owner=owner, type=type, prop=prop,
                 name=name,
                 **custom)


# Data retrieval 

def find_samples(**kwargs):
    """
    """

#def find_sample_groups(**kwargs):
#    """
#    """

def find_locations(**kwargs):
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

def find_location_types(**kwargs):
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
