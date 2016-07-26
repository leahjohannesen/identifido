import scipy.ndimage as scni
import scipy.misc as scm
import numpy as np
import os
import threading

def get_default():
    imgpath = '/data/data/notavail.jpg'
    return scni.imread(imgpath)

def breed_thread(breed, bad):
    threads = []
    breed_dir = img_dir + breed + '/'
    img_list = os.listdir(breed_dir)
    for img in img_list:
        t = threading.Thread(target=img_check, args=(img, breed_dir, bad))
        threads.append(t)
        t.start()

def img_check(img, breed_dir, bad):
    train_img_loc = breed_dir + img
    try:
        img = scni.imread(train_img_loc)
    except:
        os.remove(train_img_loc)

    try:
        diff = (img - bad).mean()
    except:
        return
    if  diff < 0.01:
        os.remove(train_img_loc)
        print 'Removed: ', train_img_loc

if __name__ == '__main__':
    img_dir = '/data/data/train/'
    dir_list = os.listdir(img_dir)

    default_img = get_default()

    for breed in dir_list:
        breed_thread(breed, default_img)
        print 'Finished breed: ', breed
