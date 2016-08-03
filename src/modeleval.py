from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
import json
import h5py
import os
import cPickle
import sys
import pandas as pd
import numpy as np

def eval(thingy, model_name):

    img_dir = data_path + thingy + '/'

    model = load_model(model_path + model_name + '/final_model.hdf5')

    # parameters
    img_height, img_width = 128, 128

    # this is the augmentation configuration we will use for training
    datagen = ImageDataGenerator(
            rescale=1./255,
            fill_mode='constant')

    gen = datagen.flow_from_directory(
            val_data_dir,
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

if __name__ == '__main__':
    model_path = '/home/ubuntu/capstone/model/'
    data_path = '/data/data/'
    
    model_name = sys.argv[2]
    test_or_all = sys.argv[1]

    out_df = eval(test_or_all, model_name)

    out_df.to_csv(model_path + model_name + '/' + test_or_all + '.csv')
