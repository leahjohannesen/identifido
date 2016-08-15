import numpy as np
from keras.models import load_model
import sys
import json
import os
from PIL import Image
import pandas as pd
import globes as G

def predict(mod_name):
    model_dir = G.MOD + mod_name + "/temp_model.hdf5"
    folder_dir = G.TST

    model = load_model(model_dir)
    
    breed_folders = sorted(os.listdir(folder_dir))
    img_pred_list = []

    for idx, breed in enumerate(breed_folders):
        print breed
        img_dir = folder_dir + breed + '/'
        img_list = os.listdir(img_dir)
        for img_loc in img_list:
            img_path = img_dir + img_loc
            img = Image.open(img_path)
            if img.mode != 'RGB':
                continue
            img = img.resize((model.input_shape[3], model.input_shape[2]))
            img = np.asarray(img, dtype='float32')
            img /= 255.
            img = np.transpose(img, (2,0,1))
            img = np.array([img])
            try:
                class_pred = model.predict(img)
            except:
                print "Pic didn't work"
                continue
            class_pred = class_pred.flatten()
            sort_pred = np.argsort(class_pred)[:-6:-1]
            if idx == sort_pred[0]:
                top1 = True
            else:
                top1 = False

            if idx in sort_pred:
                top5 = True
            else:
                top5 = False
            
            img_pred_list.append([top1,top5]) 
            
    results_df = pd.DataFrame(img_pred_list)
    
    return results_df.mean()

if __name__ == '__main__':
    mod = sys.argv[1]
    results = predict(mod)
    print results
