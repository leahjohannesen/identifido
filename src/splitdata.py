import scipy.ndimage as img
import pandas as pd
from scipy.io import loadmat
from shutil import copyfile

#sets the home directory that contains the data
home_dir = '/Users/lzkatz/Desktop/Galvanize/Capstone/'

#splits out the training images from the full list of images based on the data splits
def split_train():
    train_path = home_dir + 'rawdata/lists/train_list.mat'
    train_mat = loadmat(train_path)
    train_mat_list = train_mat['file_list'].flatten()

    #creates a list of the folders/imagenames
    train_folder_list = []
    train_img_list = []
    for name in train_mat_list:
        folder, img = name[0].split('/')
        train_img_list.append(img)
        if folder not in train_folder_list:
            train_folder_list.append(folder)

    #creates the folders to insert the images into
    for fldr in train_folder_list:
        fldr_path = home_dir + 'data/train/' + fldr
        os.mkdir(fldr_path)

    #copies the images over
    for name in train_mat_list:
        dst = home_dir + 'data/train/' + name[0]
        src = home_dir + 'rawdata/Images/' + name[0]
        copyfile(src, dst)


def split_test():
    test_path = home_dir + 'rawdata/lists/test_list.mat'
    test_mat = loadmat(test_path)
    test_mat_list = test_mat['file_list'].flatten()

    test_folder_list = []
    test_img_list = []
    for name in test_mat_list:
        folder, img = name[0].split('/')
        test_img_list.append(img)
        if folder not in test_folder_list:
            test_folder_list.append(folder)

    #creates the folders to insert the images into
    for fldr in test_folder_list:
        fldr_path = home_dir + 'data/test/' + fldr
        os.mkdir(fldr_path)

    #copies the images over
    for name in test_mat_list:
        dst = home_dir + 'data/test/' + name[0]
        src = home_dir + 'rawdata/Images/' + name[0]
        copyfile(src, dst)
