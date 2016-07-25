import scipy.ndimage as scni
import scipy.misc as scm
import numpy as np
import os
import threading

def get_default():
    # imgpath = '/data/data/notavail.jpg'
    imgpath = '/Users/lzkatz/Desktop/notavail.jpg'
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
    test_img_loc = breed_dir + img
    img = scni.imread(test_img_loc)
    try:
        diff = (img - bad).mean()
    except:
        return
    if  diff < 0.01:
        os.remove(test_img_loc)
        print 'Removed: ', test_img_loc

if __name__ == '__main__':
    img_dir = '/Users/lzkatz/Desktop/Galvanize/Capstone/Identifido/data/test/'
    dir_list = os.listdir(img_dir)

    default_img = get_default()

    for breed in dir_list:
        breed_thread(breed, default_img)
