from mongoengine import Document, DynamicDocument, DynamicEmbeddedDocument
from mongoengine import (StringField, DictField, IntField, FloatField,
                         ListField, ReferenceField, EmbeddedDocumentField,
                         DENY, MapField)

from getpass import getuser


# should we have accounting stuff?
# created, last_modified, modified_by{name,ip} ?

# how to enforce multi"column" unique constraints?

class Sample(DynamicDocument):
    uid = StringField(required=True, unique=True)
    owner = StringField(default=getuser(), required=True, unique=False)
    group = StringField(required=False, unique=False, default=None)
    #name
    #type
    # may have
    #container_id = StringField(required=True)
    #sample_position
    #sample_group_id = StringField(required=True)  # or _name?

class Container(DynamicDocument):
    uid = StringField(required=True, unique=True)
    owner = StringField(default=getuser(), required=True, unique=False)
    group = StringField(required=False, unique=False, default=None)
    #name
    #type
    #container_ref_id  # what was this again?
    # may have
    #container_id = StringField(required=True)
    # capacity
    # status
    # location

class Request(DynamicDocument):
    uid = StringField(required=True, unique=True)
    owner = StringField(default=getuser(), required=True, unique=False)
    group = StringField(required=False, unique=False, default=None)
    #sample_id
    #request_dict
    #type
    #priority
    #request_group?
    
