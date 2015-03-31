"""
ODM templates for use with samplemanager
"""
from mongoengine import Document, DynamicDocument, DynamicEmbeddedDocument
from mongoengine import (StringField, DictField, FloatField, DynamicField,
                         ReferenceField, GenericReferenceField, EmbeddedDocumentField,
                         MapField,
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

# valid sample/container/request types per beamline stored in beamlineconfig?

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


# for MapField for {container,sample,request} types
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


# for MapField for {container,sample,request} instances
class InstanceKey(DynamicEmbeddedDocument):
    """
    Describe embedded doc for SM{Sample,SampleGroup,Container,Request} properties
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

    type:  str or id?   # should this be _type_uid?
           referencefield?
        Type of an object
        Type record provides relevant common/fixed details, etc.
        Sample type: eg. pin, capillary, etc
        Container type: eg. dewar, puck, plate
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

    # does genericref take a performance hit?
    type = GenericReferenceField(required=True)

    prop = MapField(EmbeddedDocumentField(InstanceKey), required=False)

    # meta = {'allow_inheritance': True}
    # gives us "Trying to set a collection on a subclass" warnings,
    # but {'abstract': True} works
    meta = {'abstract': True, 'db_alias': ALIAS}


    def __init__(self, *args, **kwargs):
        """
        If we're not given a uid or given None or '',
        generate a new, unused uid.
        """

        DynamicDocument.__init__(self, *args, **kwargs)

        self.uid = run_on_empty(new_uid, [], {}, 'uid', **kwargs)


class SMType(SMDynDoc):
    """
    Holds info about sample, container, request, whatever types/"classes".

    Attributes
    ----------
    uid, owner, and prop inherited from SMDynDoc

    name : str
        The name of the type.

    prop_keys : dict
        dictionary of TypeKeys for the type
    """

    type = GenericReferenceField(required=False)  # overide inherited required=True
    name = StringField(required=True)
    prop_keys = MapField(EmbeddedDocumentField(TypeKey), required=False)

    meta = {'collection': 'types'}


class SMPhysicalObj(SMDynDoc):
    """
    Superclass for physical objects (containers, samples) which:

    - must have atleast one of 'identifier' or 'name'
    - must have atleast one of 'container'+'position' or 'location'

    Attributes
    ----------
    uid, owner, type, and prop inherited from SMDynDoc

    identifier : str, ~required, unique with owner
    name : str, ~optional, unique with owner

    container : bson.ObjectId, ~optional
    position : str, ~optional, unique with container

    location : str, ~optional
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

    def __check_container_pos(self, *args, **kwargs):
        try:
            if kwargs['container'] is not None and kwargs['container'] != '':
                try:
                    if kwargs['position]'] is None or kwargs['position]'] == '':
                        raise ValueError('empty position: Must specify container *and* position')
                except KeyError:
                    raise ValueError('missing position: Must specify container *and* position')
            else:
                raise ValueError('no location and empty container: Must specify atleast one of:  container+position or location')

        except KeyError:
            raise ValueError('no location and missing container: Must specify atleast one of:  container+position or location')


    def __init__(self, *args, **kwargs):
        """
        If we're not given an identifier (or given None or ''),
        but given a name, copy name to identifier.

        Atleast one of container+position or location is required.
        """
        
        # superclass __init__
        DynamicDocument.__init__(self, *args, **kwargs)  # or SMDynDoc?

        # copy 'name' to 'identifier' if needed
        run_on_empty(self.__copy_name, [self]+list(args), kwargs, 'identifier', **kwargs)

        # enforce needing one of:  location or container+position
        run_on_empty(self.__check_container_pos, [self]+list(args), kwargs, 'location', **kwargs)


    identifier = StringField(required=True)
    name = StringField()

# arg, no, self isn't right... how to do this?
# could move it into Container and Sample? :(
# or just cheese out for now and make it a genericreferencefield?
#    container = ReferenceField('self', reverse_delete_rule=DENY)
#    container = ReferenceField(Container, reverse_delete_rule=DENY)
    container = GenericReferenceField()
    position = StringField()

    location = StringField()

    meta = {'abstract': True}
    

class Container(SMPhysicalObj):
    """
    Describes a sample carrier:  dewar, puck, plate, etc. etc.

    Attributes
    ----------
    uid, owner, type, and prop and
    container, position, location inherited from SMPhysicalObj

    container properties examples:
        see common examples in SMDynDoc

        identifier:  str, unique with owner
            Short, no spaces, user supplied name/id/barcode
        name:  str, unique with owner, optional
            Longer, user supplied name

        Require identifier.
        If given only name, duplicate to identifier
        [can that be implemented in the class with identifier required=True?]


        container:  str or id?  referencefield?
            We have nested containers.  meshes in pucks in dewars...
        position:  str or ?, unique with container_uid
            Discrete, addressable location within the container

        location:  [str or id?]

        Require atleast one of:  container+position or location

        Position required if given container; doesn't
        make sense without container.

        
    example container_type properties:
        needs_nitrogen:  boolean
        capacity, layout (eg for robots),...
        robot_compatible:  boolean
        gripper_required, robot_procedure, restrictions...
        timestamp: 
            To keep track of the physical location history
        last_nitrogen_fill, next_nitrogen_fill:  timestamp
    """

    meta = {'collection': 'containers'}


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

    name = StringField(required=True)
    type = ReferenceField(SMType, required=True)

    meta = {'collection': 'samples'}
    


class Sample(SMPhysicalObj):
    """
    Holds user supplied info for samples, sample type info, to
    enable proper automated handling (pin, plate_well, capillary, ade, ...),
    and a container_uid for the container currently containing the sample.

    Attributes
    ----------
    uid, owner, type, and prop and
    container, position, location inherited from SMPhysicalObj

    properties examples:
        see common examples in SMDynDoc

        identifer:  str, unique with owner
            Short, no spaces, user supplied name/id/barcode
        name:  str, unique with owner, optional
            Longer, user supplied name

        Require identifier.
        If given only name, duplicate to identifier


        container:  str, referencefield?
            What container the sample is in.
        position:  str or ?, unique with container_uid
            Discrete, addressable location within the container

        location:  [str or id?]

        Require atleast one of:  container+position or location

        Position required if given container; doesn't
        make sense without container.


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
