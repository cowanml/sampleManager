import os
import yaml
import logging

# we should abstract this duplicated connection stuff out of all the
# nsls2 mongo apps, and really? [package].conf.[pkg]_config ?

logger = logging.getLogger(__name__)
filename = os.path.join(os.path.expanduser('~'), '.config', 'samplemanager',
                        'connection.yml')

if os.path.isfile(filename):

    with open(filename) as f:
        sm_config = yaml.load(f)

    logger.debug("Using db connection specified in config file. \n%r",
                 sm_config)

else:
    sm_config = {
        'database': 'test_sm',
        'host': "localhost",
        'port': 27017,
        }

    logger.debug("Using default db connection. \n%r",
                 sm_config)
