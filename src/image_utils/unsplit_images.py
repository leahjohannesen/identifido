import numpy as np
import os
import shutil
import sys

def copy_train():
    try:
        shutil.rmtree(all_dir)
    except:
        pass
    
    shutil.copytree(train_dir, all_dir)

def breed_condense(breed):
    all_breed_path = all_dir + breed + '/'
    val_breed_path = val_dir + breed + '/'
    test_breed_path = test_dir + breed + '/'
    val_pics = os.listdir(val_breed_path)
    test_pics = os.listdir(test_breed_path)

    for img in val_pics:
        val_img_path = val_breed_path + img
        all_img_path = all_breed_path + img
        shutil.copy2(val_img_path, all_img_path)
    for img in test_pics:
        test_img_path = test_breed_path + img
        all_img_path = all_breed_path + img
        shutil.copy2(test_img_path, all_img_path)

def condense():
    breed_list = os.listdir(all_dir)
    
    for breed in breed_list:
        breed_condense(breed)

if __name__ == '__main__':
    data_dir = '/data/data/'
    train_dir = data_dir + 'train/'
    val_dir = data_dir + 'val/'
    test_dir = data_dir + 'test/'
    all_dir = data_dir + 'all/'

    copy_train()
    condense()
