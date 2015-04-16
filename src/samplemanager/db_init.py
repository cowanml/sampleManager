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

from samplemanager import conf


from .util import new_uid
from .odm_templates import (Sample, SampleGroup, Location, Request, SMType)


logger = logging.getLogger(__name__)


def init_db():
    """
    Initialize the SampleManager db with required entries.
    """

    # basic Sample "Classes"  (eg. mesh, pin;  defines general handling procedures)
    # basic Sample "Types"  (eg. size1_mesh, spline_pin;  defines specific params)

    # Sample Group type
    sample_group_type = SMType(uid='', name='sample_group',  owner='system')
    sample_group_type.save()

    # "Named" "Samples"  (calibration foils, alignment pins, etc)


    # basic Container "Classes"  (eg. puck, plate;  defines general handling procedures)
    # basic Container "Types"  (eg. unipuck, standard_386_well_plate;  defines specific params)

    # "Named" "Containers"  (eg. robot_dewer,  containers that are part of the beamline)


    # basic Request "Types"

    # "Named" "Requests"  (eg. beamline_alignment, etc)
    # For often used, always the same (eg. parameterless), requests.
