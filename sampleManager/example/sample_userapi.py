__author__ = 'arkilic'

import random
from sampleManager.userapi.commands import create_container, add_sample
import numpy as np
import random
import string


#Define random values for multiple runs

def string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
cont_id = np.random.randint(low=0, high=1000)
cont_name = string_generator()
samp_id = np.random.randint(low=0, high=1000)
samp_name = string_generator()

#Create container and add samples

internal_cont_id = create_container(container_id=cont_id, container_name=cont_name, owner_group='arkilic', capacity=11)


add_sample(sample_id=samp_id, container_id=internal_cont_id, sample_name=samp_name, owner_group='arman',
            sample_group_name='my_group')
