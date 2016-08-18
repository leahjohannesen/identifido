import numpy as np
from keras.models import load_model
import sys
import json
import os
from PIL import Image
import pandas as pd
import globes as G
from sklearn.manifold import TSNE

def predict():
    model1_dir = G.MOD + 'deep_nodense/temp_model.hdf5'
    folder_dir = G.TST

    model1 = load_model(model1_dir)
    
    breed_folders = sorted(os.listdir(folder_dir))
    x = np.array([[]]).reshape(0,98)
    y = np.array([])

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
            except:
                print "Pic didn't work"
                continue

            x = np.append(x, class_pred1, axis=0)
            y = np.append(y, idx)
    
    print x.shape, y.shape
    print "TSNE TIME"
    np.save('tsne_x', x)
    np.save('tsne_y', y)    

    return "Done"

def tsne():
    x = np.load('tsne_x.npy')

    tsne = TSNE()

    x_trans = tsne.fit_transform(x)

    np.save('x_trans', x_trans)

if __name__ == '__main__':
    #results = predict()
    #print results
    tsne()
