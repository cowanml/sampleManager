__author__ = 'arkilic'
from sampleManager.dataapi.commands import save_container, find_container, decode_container_cursor, get_container_id
from random import randint
from sampleManager.dataapi.commands import save_sample, find_sample, decode_sample_cursor
from sampleManager.session.databaseInit import db
id = randint(0, 1000)
save_container(container_id=id, container_name='template', owner_group=0)
save_container(container_id=(id+1), container_name='template2', owner_group=0)
c_crsr = find_container({'container_id': id})
print decode_container_cursor(c_crsr)
#TODO: Test get_container_id()

cont_id = get_container_id(container_name='template')

s_id = randint(0, 1000)
save_sample(sample_id=id, container_id=cont_id, sample_name='sample1', owner_group=0)
print find_sample({'sample_id': s_id})
db.drop_collection('container')
db.drop_collection('sample')