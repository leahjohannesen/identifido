import numpy as np
from keras.models import load_model
import sys
import json
import os
from PIL import Image
import pandas as pd
import globes as G

def predict():
    model1_dir = G.MOD + 'deep_nodense/temp_model.hdf5'
    model2_dir = G.MOD + 'deep_dropout_full/temp_model.hdf5'
    model3_dir = G.MOD + 'deep_nodense_padded/temp_model.hdf5'
    model4_dir = G.MOD + 'deep_nodense_square/temp_model.hdf5'
    folder_dir = G.VAL

    model1 = load_model(model1_dir)
    model2 = load_model(model2_dir)
    model3 = load_model(model3_dir)
    model4 = load_model(model4_dir)
    
    breed_folders = sorted(os.listdir(folder_dir))
    x = np.array([[]]).reshape(0,392)
    y = np.array([[]]).reshape(0,98)

    for idx, breed in enumerate(breed_folders):
        print breed
        img_dir = folder_dir + breed + '/'
        img_list = os.listdir(img_dir)
        for img_loc in img_list:
            img_path = img_dir + img_loc
            img = Image.open(img_path)
            if img.mode != 'RGB':
                continue
            img = img.resize((model1.input_shape[3], model1.input_shape[2]))
            img = np.asarray(img, dtype='float32')
            img /= 255.
            img = np.transpose(img, (2,0,1))
            img = np.array([img])
            try:
                class_pred1 = model1.predict(img)
                class_pred2 = model2.predict(img)
                class_pred3 = model3.predict(img)
                class_pred4 = model4.predict(img)
            except:
                print "Pic didn't work"
                continue

            row_pred = np.append(class_pred1, class_pred2, axis=1)
            row_pred = np.append(row_pred, class_pred3, axis=1)
            row_pred = np.append(row_pred, class_pred4, axis=1)

            x = np.append(x, row_pred, axis=0)
            row_breed = np.zeros((1,98))
            row_breed[0,idx] = 1
            y = np.append(y, row_breed, axis=0)
    
    print x.shape, y.shape
    print "Saving"
    np.save('ens_x_val', x)
    np.save('ens_y_val', y)    

    return "Done"

if __name__ == '__main__':
    results = predict()
    print results
