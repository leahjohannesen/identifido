from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.optimizers import SGD
import json
import h5py
import os
import cPickle
from modelpy.alexnet import build_model

# model name, change each iteration
train_data_dir = '/data/data/train/'
val_data_dir = '/data/data/val/'

# parameters
nb_epoch = 50

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
        batch_size=32
        )

val_generator = val_datagen.flow_from_directory(
        val_data_dir,
        target_size=(img_width, img_height),
        batch_size=32
        )

model, model_name = build_model()

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])

# this actually fits the model
output = model.fit_generator(
        	train_generator,
        	samples_per_epoch=train_generator.N,
        	nb_epoch=nb_epoch,
        	validation_data=val_generator,
        	nb_val_samples=val_generator.N)

# creates an output folder, saves the model as a json, the weights as an hdf5, and pickles the output info
model_dir = '/home/ubuntu/capstone/model/' + model_name + '/'
os.mkdir(model_dir)

model_json = model.to_json()
open(model_dir + 'model_architecture.json', 'w').write(model_json)
model.save_weights(model_dir + 'model_weights.hd5')
