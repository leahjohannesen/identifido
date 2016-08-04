import json
import os

test_path = '/data/data/test/'

breed_list = os.listdir(test_path)

dog_dict = {}

for i, v in enumerate(breed_list):
    dog_dict[i] = v

with open('/home/ubuntu/capstone/aux_files/dog_dict.json', 'wb') as d:
    json.dump(dog_dict, d)
