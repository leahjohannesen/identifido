import re
import pandas as pd
import numpy as np
import os
import shutil
import urllib
import multiprocessing

def make_master_dir(home):
    data_dir = home + 'data/'
    test_dir = data_dir + 'test/'
    try:
        shutil.rmtree(data_dir)
    except:
        pass
    os.mkdir(data_dir)
    os.mkdir(test_dir)

def make_dog_dir(df, path):
    breeds = np.unique(df[2])
    for breed in breeds:
        breed_path = path + breed + '/'
        os.mkdir(breed_path)

def img_prep(thing):
    get_image(thing[2], thing[1], thing[0], test_dir)

def get_image(breed, link, num, test_dir):
    img_filename = test_dir + breed + '/' + str(num) + '.jpg'
    print img_filename
    try:
        urllib.urlretrieve(link, img_filename)
    except:
        pass

if __name__ == '__main__':
    home_dir = '/Users/lzkatz/Desktop/Galvanize/Capstone/Identifido/'
    csv_dir = home_dir + 'aux_files/'
    data_dir = home_dir + 'data/'
    make_master_dir(home_dir)
    test_dir = data_dir + 'test/'

    master_csv = csv_dir + 'master_list.csv'
    master_df = pd.read_table(master_csv, header=None)
    master_array = master_df.as_matrix()

    make_dog_dir(master_df, test_dir)

    core_count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(core_count)

    pool.map(img_prep, master_array)
