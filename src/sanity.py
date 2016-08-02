from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.optimizers import SGD
import json
import h5py
import os
import cPickle
import sys

#model_path = '/home/ubuntu/capstone/src/pymodels/'
#sys.path.append(model_path)
#model_filename = sys.argv[1]

#if len(model_filename) > 0:
import pymodels.basic as mod

# model name, change each iteration
train_data_dir = '/data/data/butts/train/'
val_data_dir = '/data/data/butts/val/'

# parameters
nb_epoch = 10

img_height, img_width = 128, 128

# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
        rescale=1./255,
        fill_mode='constant',
        horizontal_flip=True)

val_datagen = ImageDataGenerator(
        rescale=1./255,
        fill_mode='constant',
        horizontal_flip=True)

train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=64
        )

val_generator = val_datagen.flow_from_directory(
        val_data_dir,
        target_size=(img_width, img_height),
        batch_size=64
        )

model, model_name = mod.build_model(train_generator.nb_class)

# this actually fits the model
output = model.fit_generator(
        	train_generator,
        	samples_per_epoch=train_generator.N,
        	nb_epoch=nb_epoch,
        	validation_data=val_generator,
        	nb_val_samples=val_generator.N)

# saves the output in the model_dir
model_dir = '/home/ubuntu/capstone/model/' + 'sanity/'
os.mkdir(model_dir)

model.save(model_dir + 'final_model.hd5')
hist = output.history
params = output.params

with open(model_dir + 'history.json', 'wb') as h:
    json.dump(hist, h)
with open(model_dir + 'params.json', 'wb') as p: 
    json.dump(params, p) 
