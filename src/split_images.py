import numpy as np
import os
import shutil
import sys

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
    n_val_test = 0.2 * n_img
    val_test_array = np.random.choice(img_array, (2, n_val_test), replace=False)
    val_array = val_test_array[0]
    test_array = val_test_array[1]
   
    for img_val in val_array:
        breed_img_path = breed + '/' + img_val
        img_from = train_dir + breed_img_path
        img_to = val_dir + breed_img_path
        shutil.move(img_from, img_to)
    for img_test in test_array:
        breed_img_path = breed + '/' + img_test
        img_from = train_dir + breed_img_path
        img_to = test_dir + breed_img_path
        shutil.move(img_from, img_to)

def val_test_split():
    breed_list = os.listdir(train_dir)
    
    for breed in breed_list:
        breed_split(breed)

if __name__ == '__main__':
    data_dir = '/data/data/'
    train_dir = data_dir + 'train/'
    val_dir = data_dir + 'val/'
    test_dir = data_dir + 'test/'

    if sys.argv[1] == 'split':
        make_val_test()
        val_test_split()
    elif sys.argv[1] == 'condense':
        pass 
    else:
        pass    

    

    #val_test_split()
