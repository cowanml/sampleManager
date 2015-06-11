"""
ODM templates for use with samplemanager
"""
from mongoengine import Document, DynamicDocument, DynamicEmbeddedDocument
from mongoengine import (StringField, DictField, FloatField, DynamicField,
                         ReferenceField, GenericReferenceField, EmbeddedDocumentField,
                         MapField, BooleanField,
                         DENY)

from getpass import getuser

if __package__ is None:
    from util import (new_uid, run_on_empty)

else:
    from .util import (new_uid, run_on_empty)


ALIAS = 'sm'


# should we have accounting stuff?
#   created, last_modified, modified_by{name,ip} ?
#   location/time ?

# valid sample/location/request types per beamline stored in beamlineconfig?

# Should we make classes for well defined types (embeddeed dyn docs)?

# Can have another layer of abstraction on top of 'type', 'class', to
# gather shared props or requirements of similar types, like different
# types of dewars, pucks, pins, plates, etc.  Supported puck types
# might all share the same robot gripper, and similarly for plates but
# plates and pucks require different grippers.

# properties format:  nested dictionary
# for *_type:
#     {propname:  {dtype: [dtype], validator: [validation_func], default: [default]}
#      ...: {}}
# for an instance of that type:
#     {propname: {value: [value], source: [source], timestamp: [timestamp]}
#      ...: {}}


# for MapField for {location,sample,request} types
class TypeKey(DynamicEmbeddedDocument):
    """
    Describe embedded doc for SMType properties
    """
    desc = StringField(required=True)
    dtype = StringField(required=True,
                        choices=('integer', 'number', 'array',
                                 'boolean', 'string'))
    validator = StringField()
    default = StringField()


# for MapField for {location,sample,request} instances
class InstanceKey(DynamicEmbeddedDocument):
    """
    Describe embedded doc for SM{Sample,SampleGroup,Location,Request} properties
    """

    value = DynamicField(required=True)
    time = FloatField(required=True)

    # limit choices?  choices=('pass2',
    #   			'{staff,user}_entered_{cli,gui,web}',
    #                           '{staff,user}_imported',  # spreadsheet upload to web
    #                           'default')
    source = StringField(required=True)


# SampleManagerDynamicDocument, parent class of all the sm collections
class SMDynDoc(DynamicDocument):
    """
    Parent class for SampleManager dynamic documents.
    
    Attributes
    ----------
    uid:  str
        Globally unique id

    owner:  str or id?
        The owner, can't be unix user, might not be a matching user
        for remote... but I suppose should they later want a unix account
        might aswell reserve the matching name?

    type:  ReferenceField
        Type of an object
        Type record provides relevant common/fixed details, etc.
        Sample type: eg. pin, capillary, etc
        Location type: eg. dewar, puck, plate, room, shelf, gonio head
        Request type:  sweep, gridscan, screen

    prop:  (ie. properties)  EmbeddedDynamicDocument
        Dict of InstanceKey dicts of property values and metadata:
        # or should this be a Dict of Tuples?
        # could use value_idx=0, time_idx=1, source_idx=2 to make
        # it nearly the same...

        { 'property_name1':
          { value: dtype_of_this_property,
            time: time,
            source: str  # user input, user upload (eg spreadsheet)
          }, ...}

    properties examples:
        group:  str or id?
            Delegated privs matching PASS2.
            Do we need a more flexible role+priv system?
        status:  str, enumerated set of possible values
    """

    uid = StringField(required=True, unique=True)
    owner = StringField(required=True)

    # genericref because SMType not defined yet
    # does genericref take a performance hit?
    type = GenericReferenceField(required=True,
                                 db_field='type_id')

    prop = MapField(EmbeddedDocumentField(InstanceKey), required=False)

    # meta = {'allow_inheritance': True}
    # gives us "Trying to set a collection on a subclass" warnings,
    # but {'abstract': True} works
    meta = {'abstract': True, 'db_alias': ALIAS}


    def __init__(self, *args, **kwargs):
        """
        If we're not given a uid or given None or '',
        generate a new, unused uid.

        And dummy out owner for now... :(
        """

        DynamicDocument.__init__(self, *args, **kwargs)

        self.uid = str(run_on_empty(new_uid, [], {}, 'uid', **kwargs))
        self.owner = 'skinner'


class SMType(SMDynDoc):
    """
    Holds info about sample, location, request, whatever types/"classes".

    Attributes
    ----------
    uid, owner, and prop inherited from SMDynDoc

    type : mongoengine.ReferenceField(SMType)

    name : str, unique
        The name of the type.

    type_of : str, choices('location', 'sample', 'request', 'class'), required
    is_class : boolean, required

    prop_keys : dict, optional
        dictionary of TypeKeys for the type
    """
    # overide inherited required=True
    type = ReferenceField('self', required=False, reverse_delete_rule=DENY,
                                 db_field='type_id')

    name = StringField(required=True, unique=True)

    type_of = StringField(required=True)
    is_class = BooleanField(required=True)

    prop_keys = MapField(EmbeddedDocumentField(TypeKey), required=False)

    meta = {'collection': 'types'}


class SMPhysicalObj(SMDynDoc):
    """
    Superclass for physical objects (locations, samples) which:

    - Must have atleast one of 'identifier' or 'name'.
    - Name copied to identifier if only name given.

    Attributes
    ----------
    uid, owner, type, and prop inherited from SMDynDoc

    identifier : str, ~required, unique with owner
    name : str, ~optional, unique with owner

    location : bson.ObjectId
    position : str, optional, unique with location
    """

    def __copy_name(self, *args, **kwargs): 
        """
        identifier is required, but if name is given and not identifier,
        copy name to identifier.
        """
        try:
            if kwargs['name'] is not None and kwargs['name'] != '':
                self.identifier = kwargs['name']
        except KeyError:
            raise ValueError('Must specify atleast one of:  identifier or name')

    def __init__(self, *args, **kwargs):
        """
        If we're not given an identifier (or given None or ''),
        but given a name, copy name to identifier.
        """
        
        # superclass __init__
#        DynamicDocument.__init__(self, *args, **kwargs)  # or SMDynDoc?
        SMDynDoc.__init__(self, *args, **kwargs)  # or we don't get auto uid?

        # copy 'name' to 'identifier' if needed
        run_on_empty(self.__copy_name, [self]+list(args), kwargs, 'identifier', **kwargs)


    identifier = StringField(required=True, unique_with='owner')
    name = StringField(unique_with='owner')

    # genericref because Location not defined yet
    location = GenericReferenceField(db_field='location_id')
    position = StringField(unique_with='location_id')

    meta = {'abstract': True}
    

class Location(SMPhysicalObj):
    """
    Describes a sample carrier:  dewar, puck, plate, etc. etc.

    Attributes
    ----------
    uid, owner, type, and prop and
    location, position inherited from SMPhysicalObj

    location properties examples:
        see common examples in SMDynDoc

        identifier:  str, unique with owner
            Short, no spaces, user supplied name/id/barcode
        name:  str, unique with owner, optional
            Longer, user supplied name

        Require identifier.
        If given only name, duplicate to identifier
        [can that be implemented in the class with identifier required=True?]


        location:  referencefield
            We can have nested locations/containers.  meshes in pucks in dewars...
        position:  str, unique with location
            Discrete, addressable position within a location/container

    example location_type properties:
        needs_nitrogen:  boolean
        capacity, layout (eg for robots),...
        robot_compatible:  boolean
        gripper_required, robot_procedure, restrictions...
        timestamp: 
            To keep track of the physical location history
        last_nitrogen_fill, next_nitrogen_fill:  timestamp
    """

    meta = {'collection': 'locations'}


# not quite fully baked?
class SampleGroup(SMDynDoc):
    """
    Holds info about related groups of samples.

    eg. For measurements requiring multiple samples to complete,
    like tiny crystals which are destroyed before a full dataset
    can be collected... need lots of the tiny crystals, and this data
    structure to store overall completeness information, etc.

    Attributes
    ----------
    uid, owner, type, and prop inherited from SMDynDoc

    name : str, unique with owner
    """

    # Maybe isinstance to check 'type' is a sample_group type?
    # Should default to a ref to a 'generic_sample_group' type entry, 
    # which has a parent type of 'sample_group_type' or something?

    name = StringField(required=True, unique_with='owner')
    type = ReferenceField(SMType, required=True, reverse_delete_rule=DENY,
                          db_field='type_id')

    meta = {'collection': 'samples'}
    


class Sample(SMPhysicalObj):
    """
    Holds user supplied info for samples, sample type info, to
    enable proper automated handling (pin, plate_well, capillary, ade, ...),
    and a location id for the location currently containing the sample.

    Attributes
    ----------
    uid, owner, type, and prop and
    location, position inherited from SMPhysicalObj

    properties examples:
        see common examples in SMDynDoc

        identifer:  str, unique with owner
            Short, no spaces, user supplied name/id/barcode
        name:  str, unique with owner, optional
            Longer, user supplied name

        Require identifier.
        If given only name, duplicate to identifier


        location:  referencefield
            What location/container the sample is in.
        position:  str, unique with location
            Discrete, addressable position within the location/container

    example sample_type properties:
        sample_group:  ReferenceField
        robot_compatible:  boolean
        gripper_required, robot_procedure, restrictions...
        uses_coldstream:  boolean
    """

    meta = {'collection': 'samples'}


class Request(SMDynDoc):
    """
    Holds requested measurements, request type info, to enable proper
    automation and a sample_uid for the sample to measure.

    If a sample is involved...?  To realize the moonshot goal of Qmx
    (all beamline operations done asynchronously. enable interleaving users!
    enables moving processing/planning/thought off of beamtime),
    this should be able to hold *any* beamline operation.

    Attributes
    ----------
    uid, owner, type, and prop inherited from SMDynDoc

    request properties examples:
        see common examples in SMDynDoc

        measurement params and automation criteria appropriate for request type

        sample_uid:  id,  referencefield?
            Sample to take the measurement on
        sample_group_uid:  str or id?  referencefield?
            Linking identifier for multisample measurements.
            eg. measuring overall completeness with many tiny crystals

        request_group_uid:  str or id?  referencefield?
            Linking identifier for multipart/multisample measurements.
            eg. to enable reprioritizing or aborting a set of
            related requests

        priority:
            Field enabling arbitrary request queue ordering

    example request_type properties:
        start, end, increment

        beamsize, gridsize

        autocollect_threshold
    """

    meta = {'collection': 'requests'}


collections = [SMType, Location, Sample, Request]
