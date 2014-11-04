__author__ = 'arkilic'

from sampleManager.dataapi.commands import save_container, find_container, decode_container_cursor, get_container_mongo_id
from random import randint
from sampleManager.dataapi.commands import save_sample, find_sample, decode_sample_cursor
from sampleManager.dataapi.commands import save_request, find_request, decode_request_cursor, get_sample_mongo_id, \
    get_request_mongo_id, save_multiple_containers
import random
import string


def string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#Container Insert/Query Test
id = randint(0, 10000)

cont_name = string_generator()

save_container(container_id=id, container_name=cont_name, owner_group='arkilic', capacity=5, status='Active')

c_crsr = find_container({'container_id': id})

entry = decode_container_cursor(c_crsr)

cont_id = get_container_mongo_id(container_name=cont_name)

if cont_id == entry[cont_name]['_id']:
    print 'save_container() test passed'
    print 'get_container_id() test passed'
else:
    raise Exception('get_container_id test failed')


#Sample Insert/Query Test
s_id = randint(0, 10000)
samp_name = string_generator()
save_sample(sample_id=s_id, container_id=cont_id, sample_name=samp_name, owner_group='0', sample_position=1,
            sample_group_name='my_group')

s_crsr = find_sample({'sample_id': s_id})

entry = decode_sample_cursor(sample_cursor=s_crsr)

samp_id = get_sample_mongo_id(sample_name=samp_name)

if samp_id == entry[samp_name]['_id']:
    print 'save_sample() test passed'
    print 'get_sample_mongo_id() test passed'
else:
    raise Exception('get_sample_mongo_id test failed')


#Request Insert/Query Test
r_id = randint(0, 1000)

save_request(sample_id=samp_id, request_dict={'property1': 12.3, 'property_2': 'some_value1'}, request_id=r_id, priority='High')
r_crsr = find_request({'request_id': r_id})

entry = decode_request_cursor(request_cursor=r_crsr)

r_id = get_request_mongo_id(request_id=r_id)


#Sample position test
id = randint(0, 10000)

s_id = randint(0, 10000)

cont_name = string_generator()

c_id = save_container(container_id=id, container_name=cont_name, owner_group='0', container_ref_id=cont_id,capacity=12)

save_sample(sample_id=s_id, container_id=c_id, sample_name=samp_name+'sf', owner_group='0', sample_position=12,
            sample_group_name='my_sample_group')

save_sample(sample_id=s_id+1, container_id=c_id, sample_name=samp_name+'sf2', owner_group='0', sample_position=9,
            sample_group_name='my_sample_group')
