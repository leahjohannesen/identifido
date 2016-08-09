import globes as G
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
import json
import h5py
import os
import cPickle
import sys
import pandas as pd
import numpy as np

def eval(tvta, torf, model_name):

    img_dir = G.DAT + tvta + '/'

    if torf == 'temp':
        temp_or_final = '/temp_model.hdf5' 
    else:
        temp_or_final = '/final_model.hdf5'
    model = load_model(G.MOD + model_name + temp_or_final)



    # parameters
    img_height, img_width = 128, 128

    # this is the augmentation configuration we will use for training
    datagen = ImageDataGenerator(
            rescale=1./255,
            fill_mode='constant')

    gen = datagen.flow_from_directory(
            img_dir,
            target_size=(img_width, img_height),
            batch_size=64,
            shuffle=False
            )

    actual = gen.classes
    predict = model.predict_generator(gen, gen.N)
    
    arr = actual[:, np.newaxis]
    final_arr = np.append(arr, arr, axis=1)

    for idx in xrange(len(actual)):
        final_arr[idx,1] = np.argmax(predict[idx])
        
    df = pd.DataFrame(final_arr, columns=['actual', 'pred'])    
    
    return df

def make_csv(tvta, df):
    out_path = G.MOD + model_name + '/' + test_or_all + '_' + tvta + '.csv'
    df.to_csv(out_path, header=False)

if __name__ == '__main__':
    temp_or_final = sys.argv[1]
    model_name = sys.argv[2]

    blah = ['train', 'val', 'test', 'all']
    for i in blah:
        df = eval(blah, temp_or_final, model_name)
        make_csv(blah, df)   
