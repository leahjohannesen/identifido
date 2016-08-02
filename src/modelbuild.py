from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint
import json
import h5py
import os
import cPickle
import sys

model_path = '/home/ubuntu/capstone/src/pymodels/'
sys.path.append(model_path)
model_filename = sys.argv[1]

if len(model_filename) > 0:
    mod = __import__(model_filename)

# model name, change each iteration
train_data_dir = '/data/data/train/'
val_data_dir = '/data/data/val/'

# parameters
nb_epoch = 25

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

# saves the output in the model_dir
model_dir = '/home/ubuntu/capstone/model/' + model_name + '/'
os.mkdir(model_dir)
temp_path = model_dir + 'temp_model.hdf5'

#update the model if stuff gets better
checkpointer = ModelCheckpoint(filepath=temp_path, verbose=1, save_best_only=True)

# this actually fits the model
output = model.fit_generator(
        	train_generator,
        	samples_per_epoch=train_generator.N,
        	nb_epoch=nb_epoch,
        	validation_data=val_generator,
        	nb_val_samples=val_generator.N,
                callbacks=[checkpointer])

model.save(model_dir + 'final_model.hdf5')
