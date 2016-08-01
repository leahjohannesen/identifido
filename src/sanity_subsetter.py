import os
import numpy as np
import sys
import shutil

def split(name, n_breed=10, n_pics=0.1):
    data_dir = '/data/data/'
    train_dir = data_dir + 'train/'
    val_dir = data_dir + 'val/'
    sub_dir = data_dir + name + '/'
    new_train = sub_dir + 'train/'
    new_val = sub_dir + 'val/'    

    try:
        shutil.rmtree(sub_dir)
    except:
        pass
    os.mkdir(sub_dir)
    os.mkdir(new_train)
    os.mkdir(new_val)

    breed_list = np.array(os.listdir(train_dir))
    random_breeds = np.random.choice(breed_list, n_breed, replace=False)
    
    for breed in random_breeds:
        breed_train_dir = train_dir + breed + '/'
        breed_val_dir = val_dir + breed + '/'
        new_breed_train_dir = new_train + breed + '/'
        new_breed_val_dir = new_val + breed + '/'

        os.mkdir(new_breed_train_dir)
        os.mkdir(new_breed_val_dir)

        train_list = os.listdir(breed_train_dir)
        n_train = int(len(train_list)*n_pics)
        random_train = np.random.choice(train_list, n_train, replace=False)
        for pic in random_train:
            pic_path = breed_train_dir + pic
            pic_path_new = sub_dir + 'train/' + breed + '/'
            shutil.copy2(pic_path, pic_path_new)
        
        val_list = os.listdir(breed_val_dir)
        n_val = int(len(val_list)*n_pics)
        random_val = np.random.choice(val_list, n_val, replace=False)
        for pic in random_val:
            pic_path = breed_val_dir + pic
            pic_path_new = sub_dir + 'val/' + breed + '/'
            shutil.copy2(pic_path, pic_path_new)

if __name__ == '__main__':
    folder_name = sys.argv[1]
    n_breeds = int(sys.argv[2])
    per_pics = int(sys.argv[3])/100.
    split(folder_name, n_breeds, per_pics)
