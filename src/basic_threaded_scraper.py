from bs4 import BeautifulSoup
import requests
import string
import re
import pandas as pd
import numpy as np
import os
import shutil
import urllib
import multiprocessing

def make_dir(outer_dir, dir_name):
    dir_path = outer_dir + dir_name + '/'
    try:
        shutil.rmtree(dir_path)
    except:
        pass
    os.mkdir(dir_path)
    return dir_path

def breed_prep(csv_name, csv_path, out_path):
    breed_name = re.sub('.csv|\s','', csv_name)
    breed_path = make_dir(out_path, breed_name)
    breed_df = pd.read_csv(csv_path + csv_name, header=None, names=['Link'], index_col=0)
    img_nums = breed_df.index
    img_urls = breed_df.values.flatten()
    print "{} path created.".format(breed_name)
    return breed_name, breed_path, img_nums[:2], img_urls[:2]

def get_image((breed_name, breed_path, img_num, img_url)):
    img_filename = breed_path + breed_name + str(img_num) + '.jpg'
    try:
        urllib.urlretrieve(img_url, img_filename)
    except:
        pass


if __name__ == '__main__':
    csv_dir = '/Users/lzkatz/Desktop/Galvanize/Capstone/Identifido/aux_files/img_list/'
    data_dir = '/Users/lzkatz/Desktop/Galvanize/Capstone/Identifido/data/'
    test_path = make_dir(data_dir, 'test')

    core_count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(core_count)

    file_list = os.listdir(csv_dir)
    for breed_file in file_list:
        breed_name, breed_path, breed_img_nums, breed_img_urls = breed_prep(breed_file, csv_dir, test_path)
        #stupid stuff to masic basic threading work
        n = len(breed_img_nums)
        tuple_arg = zip([breed_name]*n, [breed_path]*n, breed_img_nums, breed_img_urls)
        pool.map(get_image, tuple_arg)
