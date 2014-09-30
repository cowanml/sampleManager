__author__ = 'arkilic'
from sampleManager.dataapi.commands import save_container
from random import randint


id = randint(0,1000)
save_container(container_id=id, container_name='template', owner_group=0, item_list=['item0', 'item1'])