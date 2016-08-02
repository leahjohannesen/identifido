import re
import pandas as pd
import numpy as np
import os
import shutil
import urllib2
import multiprocessing
import threading
import time

open_docs = 10000

def make_master_dir(home):
    print 'Making home dir'
    data_dir = home + 'data/'
    train_dir = data_dir + 'train/'
    try:
        shutil.rmtree(data_dir)
    except:
        pass
    os.mkdir(data_dir)
    os.mkdir(train_dir)

def make_dog_dir(df, path):
    print 'Making dog dirs'
    breeds = np.unique(df[2])
    for breed in breeds:
        breed_path = path + breed + '/'
        os.mkdir(breed_path)

def img_threader(sub_array):
    threads = []
    for row in sub_array:
        t = threading.Thread(target=get_img, args=(row[2],row[1],row[0],train_dir))         
        threads.append(t)
        while threading.active_count() > open_docs - 500: 
            time.sleep(10)
        t.start()

def get_img(breed, link, num, train_dir):
    img_filename = train_dir + breed + '/' + str(num) + '.jpg'

    #for trying to get links, if it breaks, it skips the open portion
    try:
        img_link = urllib2.urlopen(link)
    except:  
        return
    
    if num % 100 == 0:
        print 'Breed: {}, Pic: {}'.format(breed,num)
    f = open(img_filename, 'wb')
    f.write(img_link.read())
    f.close()

if __name__ == '__main__':
    home_dir = '/home/ubuntu/capstone/'
    csv_dir = home_dir + 'aux_files/'
    mount_dir = '/data/' 
    make_master_dir(mount_dir)
    data_dir = mount_dir + 'data/'
    train_dir = data_dir + 'train/'

    master_csv = csv_dir + 'master_list.csv'
    master_df = pd.read_table(master_csv, header=None)
    master_array = master_df.as_matrix()

    make_dog_dir(master_df, train_dir)

    #core_count = multiprocessing.cpu_count()
    #pool = multiprocessing.Pool(core_count)
   
    #split_master_array = np.split(master_array, core_count)
    #pool.map(img_threader, split_master_array)
   
    img_threader(master_array)
