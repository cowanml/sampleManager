from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import six
import datetime
import logging
import uuid
from functools import wraps
from mongoengine import connect

from metadatastore.document import Document
from metadatastore.commands import (db_connect, db_disconnect, _ensure_connection,
                                    _normalize_object_id, _format_time)

from sampleManager import conf


from .util import new_uuid
from .odm_templates import (Sample, SampleGroup, Container, Request, SMType)


logger = logging.getLogger(__name__)


def init_db():
    """
    Initialize the SampleManager db with required entries.
    """
    
    # Sample Group
    sample_group_type = SMType(
