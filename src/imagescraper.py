from bs4 import BeautifulSoup
import requests
import string
import re
import pandas as pd
import numpy as np
import os
import shutil
import urllib

csv_dir = '/Users/lzkatz/Desktop/Galvanize/Capstone/Identifido/aux_files/img_list/'
data_dir = '/Users/lzkatz/Desktop/Galvanize/Capstone/Identifido/data/'

def make_dir():
    test_dir = data_dir + 'test/'
    try:
        shutil.rmtree(test_dir)
    except:
        pass
    os.mkdir(test_dir)


def image_scrape_test():
    test_dir = data_dir + 'test/'
    file_list = os.listdir(csv_dir)
    for breed in file_list:
        breed_name = re.sub('.csv|\s','', breed)
        breed_dir = test_dir + breed_name + '/'
        os.mkdir(breed_dir)
        breed_ser = pd.read_csv(csv_dir + breed, header=None, names=['Link'], index_col=0)
        counter = 0
        print "Scraping for {}.".format(breed_name)
        for n, link in enumerate(breed_ser['Link'].values):
            if counter > 2: break
            img_filename = breed_dir + breed_name + str(n) + '.jpg'
            try:
                urllib.urlretrieve(link, img_filename)
            except:
                pass
            counter += 1
        print "Breed complete."

if __name__ == '__main__':
    make_dir()
    image_scrape_test()
