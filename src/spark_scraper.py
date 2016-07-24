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
import pyspark as ps

def make_master_dir(home):
    data_dir = home + 'data/'
    test_dir = data_dir + 'test/'
    try:
        shutil.rmtree(data_dir)
    except:
        pass
    os.mkdir(data_dir)
    os.mkdir(test_dir)

def make_dog_dir(breed):
    os.mkdir(breed + '/')

def get_image(breed, link, num, test_dir):
    img_filename = test_dir + breed + '/' + str(num) + '.jpg'
    try:
        urllib.urlretrieve(link, img_filename)
    except:
        pass


if __name__ == '__main__':
    sc = ps.SparkContext('local[4]')

    home_dir = '/Users/lzkatz/Desktop/Galvanize/Capstone/Identifido/'
    csv_dir = home_dir + 'aux_files/'
    data_dir = home_dir + 'data/'
    make_master_dir(home_dir)
    test_dir = data_dir + 'test/'

    master_df = csv_dir + 'master_list.csv'


    file_rdd = sc.textFile(master_df, 30)

    split_rdd = file_rdd.map(lambda line: line.split('\t'))

    folder_rdd = split_rdd.map(lambda line: line[2])\
        .distinct()\
        .map(lambda breed: os.mkdir(test_dir + breed + '/'))\
        .collect()

    scrape_rdd = split_rdd.map(lambda img: (img[2], img[1], img[0]))\
        .map(lambda link: get_image(link[0],link[1], link[2], test_dir))\
        .collect()
