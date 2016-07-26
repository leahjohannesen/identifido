import numpy as np
import os
import shutil

def make_val_test():
    try:
        shutil.rmtree(val_dir)
        shutil.rmtree(test_dir)
    except:
        pass

    os.mkdir(val_dir)
    os.mkdir(test_dir)

    breed_list = os.listdir(train_dir)
    for breed in breed_list:
        os.mkdir(val_dir + breed)
        os.mkdir(test_dir + breed)

def breed_split(breed):
    img_list = os.listdir(train_dir + breed + '/')
    img_array = np.array(img_list)
    n_img = len(img_array)
    
    

def val_test_split():
    breed_list = os.listdir(train_dir)
    
    for breed in breed_list:
        breed_split(breed)

if __name__ == '__main__':
    data_dir = '/data/data/'
    train_dir = data_dir + 'train/'
    val_dir = data_dir + 'val/'
    test_dir = data_dir + 'test/'

    make_val_test()

    val_test_split()
