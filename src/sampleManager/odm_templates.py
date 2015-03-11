"""
ODM templates for use with samplemanager
"""
from mongoengine import Document, DynamicDocument, DynamicEmbeddedDocument
from mongoengine import (StringField, DictField, IntField, FloatField,
                         ListField, ReferenceField, EmbeddedDocumentField,
                         DENY, MapField)

from getpass import getuser


# should we have accounting stuff?
#   created, last_modified, modified_by{name,ip} ?
#   location/time ?

# valid sample/container/request types per beamline stored in beamlineconfig?



# Only omnipresent, required, not null fields in top level.
# All varied or optional fields go in a whatever_props embedded doc.
# But still use DynamicDocument... the only constant is change...

# Should we make classes for well defined types (embeddeed dyn docs)?

# Store "type" info in the related collections.  eg. sample_types are
# just "samples" with type='sample_type'.  Sparse index on
# whatever_type to quickly access.  Props for types define props for
# instances of that type.  Can have another layer of abstraction on
# top of 'type', 'class', to gather shared props or requirements of
# similar types, like different types of dewars, pucks, pins, plates,
# etc.  Supported puck types might all share the same robot gripper,
# and similarly for plates but plates and pucks require different grippers.

# hrm... this kinda degenerated.  why have 3 collections?




class TypeKey(DynamicEmbeddedDocument):
    """
    """

    dtype = StringField(required=True,
                        choices=('integer', 'number', 'array',
                                 'boolean', 'string'))
    validator = StringField()
    default = StringField()


class InstanceKey(DynamicEmbeddedDocument):
    """
    """

    value = DynamicField(required=True)
    source = StringField(required=True)
    time = FloatField(required=True)


# SampleManagerDynamicDocument
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

    properties:  EmbeddedDynamicDocument
        Put everything optional/varying in here.

    properties examples:
        group:  str or id?
            Delegated privs matching PASS2.
            Do we need a more flexible role+priv system?
        status:  str, enumerated set of possible values

    properties format:  nested dictionary
    for *_type:
        {propname:  {dtype: [dtype], validator: [validation_func], default: [default]}
         ...: {}}
    for an instance of that type:
        {propname: {value: [value], source: [source], timestamp: [timestamp]}
         ...: {}}
    """

    uid = StringField(required=True, unique=True)
    owner = StringField(required=True)

    # does genericref take a performance hit?
    type = GenericReferenceField(required=True)

    properties = DictField(required=True)

    meta = {'allow_inheritance': True}  # or is {'abstract': True} better?


class Container(SMDynDoc):
    """
    Describes a sample carrier:  dewar, puck, plate, etc. etc.

    Attributes
    ----------
    uid, owner, type, and properties inherited from SMDynDoc

    container properties examples:
        see common examples in SMDynDoc

        identifier:  str, unique with owner
            Short, no spaces, user supplied name/id/barcode, optional?
        name:  str, unique with owner
            Longer, user supplied name, optional?

        container_uid:  str or id?  referencefield?
            We have nested containers.  pins in pucks in dewars...
        position:  str or ?, unique with container_uid
            Discrete, addressable location within the container

        location:  str or id?
        timestamp: 
            To keep track of the physical location history

        last_nitrogen_fill, next_nitrogen_fill:  timestamp

    example container_type properties:
        needs_nitrogen:  boolean
        capacity, layout (eg for robots),...
        robot_compatible:  boolean
        gripper_required, robot_procedure, restrictions...
    """

    meta = {'collection': 'container'}


class SampleKeys(DynamicEmbeddedDocument):
    """
    Required property definitions for sample types.

    properties examples:
        see common examples in SMDynDoc

        identifer:  str, unique with owner
            Short, no spaces, user supplied name/id/barcode, optional?
        name:  str, unique with owner
            Longer, user supplied name, optional?

        container:  str, referencefield?
            What container the sample is in.
        position:  str or ?, unique with container_uid
            Discrete, addressable location within the container

        sample_group:  referencefield?
            Linking identifier for multisample measurements.
            eg. measuring overall completeness with many tiny crystals

    example sample_type properties:
        robot_compatible:  boolean
        gripper_required, robot_procedure, restrictions...
        uses_coldstream:  boolean
    """

    #identifier = StringField(required=True)
    name = StringField(required=True)

    #container = ReferenceField(Container, db_field='container_id')
    #position = StringField(required=True)
    # need a way to specify validation for position...
 
    # hrm... maybe a better way to do this?
    #sample_group = ReferenceField(Sample, db_field='sample_id', required=False)
    

class SMType(SMDynDoc):
    """
    Holds user supplied info for samples, sample type info, to
    enable proper automated handling (pin, plate_well, capillary, ade, ...),
    and a container_uid for the container currently containing the sample.

    Attributes
    ----------
    uid, owner, type, and properties inherited from SMDynDoc

    name : str
        The name of the sample type.
    """

    name = StringField(required=True)
    properties = MapField(EmbeddedDocumentField(TypeKey), required=True)

    meta = {'collection': 'types'}


class Sample(SMDynDoc):
    """
    Holds user supplied info for samples, sample type info, to
    enable proper automated handling (pin, plate_well, capillary, ade, ...),
    and a container_uid for the container currently containing the sample.

    Attributes
    ----------
    uid, owner, type, and properties inherited from SMDynDoc

    properties examples:
        see common examples in SMDynDoc

        identifer:  str, unique with owner
            Short, no spaces, user supplied name/id/barcode, optional?
        name:  str, unique with owner
            Longer, user supplied name, optional?

        container_uid:  str, referencefield?
            What container the sample is in.
        position:  str or ?, unique with container_uid
            Discrete, addressable location within the container

        sample_group_uid:  str or id?  referencefield?
            Linking identifier for multisample measurements.
            eg. measuring overall completeness with many tiny crystals

    example sample_type properties:
        robot_compatible:  boolean
        gripper_required, robot_procedure, restrictions...
        uses_coldstream:  boolean
    """

    meta = {'collection': 'sample'}


class Request(SMDynDock):
    """
    Holds requested measurements, request type info, to enable proper
    automation and a sample_uid for the sample to measure.

    If a sample is involved...?  To realize the moonshot goal of Qmx
    (all beamline operations done asynchronously. enable interleaving users!
    enables moving processing/planning/thought off of beamtime),
    this should be able to hold *any* beamline operation.

    Attributes
    ----------
    uid, owner, type, and properties inherited from SMDynDoc

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

    meta = {'collection': 'request'}
