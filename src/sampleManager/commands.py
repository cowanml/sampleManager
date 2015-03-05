from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import six
import datetime
import logging
import uuid
from functools import wraps
from mongoengine import connect

from metadatastore.document import Document

#from .odm_templates import (RunStart, BeamlineConfig, RunStop,
#                            EventDescriptor, Event, DataKey)


logger = logging.getLogger(__name__)

