import logging

from metadatastore.conf import load_configuration


logger = logging.getLogger(__name__)

(db_connect_args, ALIAS, timezone, other
        ) = load_configuration('samplemanager', 'SM')

