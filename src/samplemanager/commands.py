from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six
import datetime
import logging
import uuid
import functools
import itertools

from mongoengine import connect

from metadatastore.commands import ensure_connection
from metadatastore.commands import (_normalize_object_id,
                                    _format_time,
                                    _AsDocument)

from . import conf
from .conf import ALIAS


from .util import (new_uid, get_owner, check_and_insert_key)
from .odm_templates import (Sample, Location, Request, SMType)


logger = logging.getLogger(__name__)

def debug_connection(conf=conf):
    print(conf.db_connect_args)
    return ensure_connection(conf=conf)

#_ensure_connection = ensure_connection(conf=conf)
_ensure_connection = debug_connection(conf=conf)


# Data retrieval 

# hrm... not sure this is better than the bunch of small
# duplications it avoided?
@_ensure_connection
def _generic_query(**kwargs):
    """
    """

    required_args = ['class_', 'pop_ids', 'norm_ids']
    for arg in required_args:
        try:
            kwargs[arg]
        except KeyError:
            raise KeyError('query failed to provide required arg: ' + str(arg))
    

    # pop class_ from kwargs passed on
    class_ = kwargs.pop('class_')


    # Fetch and use _id's of these object kwargs.
    # (And remove pop_ids from kwargs passed on.)
    for arg in kwargs.pop('pop_ids'):
        try:
            kwargs[arg] = kwargs.pop(arg).id
        except KeyError:
            pass  # might be an optional arg?


    # normalize these id fields/ref fields in query
    # (And remove norm_ids from kwargs passed on.)
    for arg in kwargs.pop('norm_ids'):
        _normalize_object_id(kwargs, arg)


    # standardize time
    _format_time(kwargs)


    # pop optional order_by from kwargs passed on
    try:
        order_by = kwargs.pop('order_by')
    except KeyError:
        order_by = 'time'


    objects = class_.objects(__raw__=kwargs).order_by(order_by)

    _as_document = _AsDocument()

    for obj in objects:
        yield _as_document(obj)
    

# what's next?  a query factory to further avoid duplication? :(
# One off code bits in mds queries not captured so far in _generic_query:
#    - replace_data_key_dots type stuff
#    - user friendly error msgs for easy mistakes        
# and it would really only work for base queries of the 4 base types anyway

# what about *_id's in props which should be popped or normalized?
# what about order by of props?

# what about owner!?

# recursively_find_X? eg. to find all the samples nested in a location?

# how is mongo deref'ing not like a join? is it recursive?
# seems more like uber-auto-joins, and yes recursive to selectable depth
# via 'select_related'.  We're kinda losing most of that :(

# check https://mongoengine-odm.readthedocs.org/guide/querying.html#getting-related-data
# auto derefs listfield and dictfield!?

# can it query across refs?  no

# !!only need refs the other way when things move rather than just change?
# cuz can't atomically do both parts of a move.
# or for better performance of queries on what would be subdocs?

# !!why doesn't mds use embedded docs?  they don't move stuff?

# look at https://mongoengine-odm.readthedocs.org/guide/querying.html#custom-querysets

# object "class" lists instead of inheritence? https://mongoengine-odm.readthedocs.org/guide/querying.html#querying-lists


### these are actually function definitions!
### and X.__doc__ is their docstring!


# see the def of _generic_query to understand these kwargs

kwargs = {'pop_ids': ['type_id'], 'norm_ids': ['_id']}

find_requests = functools.partial(_generic_query,
                                  class_=Request,
                                  **kwargs)
find_requests.__name__ = 'find_requests'
find_requests.__doc__ = """"""


kwargs['order_by'] = 'type_id, name'

# do we need this?
find_types = functools.partial(_generic_query,
                               class_=SMType,
                               **kwargs)
find_types.__name__ = 'find_types'
find_types.__doc__ = """"""


kwargs['pop_ids'].append('location_id')

find_samples = functools.partial(_generic_query,
                                 class_=Sample,
                                 **kwargs)
find_samples.__name__ = 'find_samples'
find_samples.__doc__ = """"""


find_locations = functools.partial(_generic_query,
                                   class_=Location,
                                   **kwargs)
find_locations.__name__ = 'find_locations'
find_locations.__doc__ = """"""





#def find_sample_groups(**kwargs):
#    """
#    """



# type/class query and insertion
@_ensure_connection
def _insert_type(uid=None, owner=None, type=None, prop=None,
                 name=None,
                 type_of=None, is_class=False,
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

    type_of : str, choices('location', 'sample', 'request', 'class'), required
    is_class : boolean, required

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

    if custom is None:
        custom = {}

    print(type)

    sm_type = SMType(uid=uid, owner=owner, type=type, prop=prop,
                     name=name,
                     type_of=type_of, is_class=is_class,
                     prop_keys=prop_keys,
                     **custom)

    sm_type.save(validate=True, write_concert={"w": 1})
    logger.debug('Inserted SMType with uid %s', sm_type.uid)

    return sm_type
    

@_ensure_connection
def _make_typeclass_routines(type_of):
    """
    return a type and class finder given an object type

    Parameters
    __________
    type_of : str
        eg. 'location', 'sample', 'request' (maybe 'type'?)
    """

    def _make_finder(type_of, is_class):

        def _new_finder(**kwargs):
            ########
            check_and_insert_key('type_of', kwargs, type_of)
            check_and_insert_key('is_class', kwargs, is_class)
        
            for result in _generic_query(class_=SMType,
                                         pop_ids=['type_id'],
                                         norm_ids=['_id'],
                                         order_by='type_id, name',
                                         **kwargs):
                yield result
            ########

        what = "classes" if is_class else "types"
    
        _new_finder.func_name = str('find_' + str(type_of) + '_' + what)
        _new_finder.__doc__ = ("find all " + what + " where type_of=='" + 
                               str(type_of))
                               # append more complete docstring here
        return _new_finder


    def _make_inserter(type_of, is_class):

        def _new_inserter(uid=None, owner=None, type=None, prop=None,
                          name=None,
                          type_of=None, is_class=None,
                          custom=None
                          ):
            ########
#            type = find_types()  # ?

            if custom is None:
                custom = {}

            _insert_type(uid=uid, owner=owner, type=type, prop=prop,
                         name=name,
                         type_of=type_of, is_class=is_class,
                         **custom)
            ########

        what = "class" if is_class else "type"
    
        _new_inserter.func_name = str('insert_' + str(type_of) + '_' + what)
        _new_inserter.__doc__ = ("insert a new "+
                               str(type_of) + ' ' + what)
                               # append more complete docstring here
        return _new_inserter


    return(itertools.chain(map(_make_finder, [type_of]*2, [True, False]),
                           map(_make_inserter, [type_of]*2, [True, False])))


# make find+insert routines for sample/location/request types/classes

(find_sample_types, find_sample_classes,
 insert_sample_type, insert_sample_class
        ) = _make_typeclass_routines('sample')

(find_location_types, find_location_classes,
 insert_location_type, insert_location_class
        ) = _make_typeclass_routines('location')

(find_request_types, find_request_classes,
 insert_request_type, insert_request_class
        ) = _make_typeclass_routines('request')



# Data insertion/modification

@_ensure_connection
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

    if custom is None:
        custom = {}

    sample = Sample(uid=uid, owner=owner, type=type, prop=prop,
                    name=name, identifier=identifier,
                    location=location, position=position,
                    **custom)

    sample.save(validate=True, write_concert={"w": 1})
    logger.debug('Inserted Sample with uid %s', sample.uid)

    return sample


# not quite fully baked...
@_ensure_connection
def insert_sample_group(uid=None, owner=None, type=None, prop=None,
                        name=None, custom=None):
    """
    Holds info about related groups of samples.

    eg. For measurements requiring multiple samples to complete,
    like tiny crystals which are destroyed before a full dataset
    can be collected... need lots of the tiny crystals, and this data
    structure to store overall completeness information, etc.

    Parameters
    ----------
    uid, owner, type, and prop : inherited from SMDynDoc

    name : str
       A short, human readable, name for the sample group.
    
    """

    if custom is None:
        custom = {}

    sample_group = SampleGroup(uid=uid, owner=owner, type=type, prop=prop,
                     name=name, **custom)

    sample_group.save(validate=True, write_concert={"w": 1})
    logger.debug('Inserted Sample Group with uid %s', sample_group.uid)

    return sample_group
    

@_ensure_connection
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


@_ensure_connection
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

    if custom is None:
        custom = {}

    request = Request(uid=uid, owner=owner, type=type, prop=prop,
                          **custom)

    request.save(validate=True, write_concert={"w": 1})
    logger.debug('Inserted Request with uid %s', request.uid)

    return request

# a way to make reusable requests?
#def insert_named_request():

## request view
# get the priority sorted request list for anything in the primary dewar
## dewar view
# show me all samples in all the pucks in the primary dewar

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
