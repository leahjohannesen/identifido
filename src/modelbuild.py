from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.optimizers import SGD
import json
import h5py
import os
import cPickle

# model name, change each iteration
train_data_dir = '/data/data/train/'
val_data_dir = '/data/data/val/'

# dimensions of our images.
img_width, img_height = 200, 200

# parameters
nb_epoch = 10

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
        batch_size=100
        )

val_generator = val_datagen.flow_from_directory(
        val_data_dir,
        target_size=(img_width, img_height),
        batch_size=50
        )

model = Sequential()
model.add(Convolution2D(32, 3, 3, input_shape=(3, img_width, img_height)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(32, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(64, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(train_generator.nb_class))
model.add(Activation('softmax'))

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
curr_last = os.listdir('/home/ubuntu/capstone/model/')[-1]
new_num = str(int(curr_last[5:]) + 1)
model_dir = '/home/ubuntu/capstone/model/model' + new_num + '/'
os.mkdir(model_dir)

model_json = model.to_json()
open(model_dir + 'model_architecture.json', 'w').write(model_json)
model.save_weights(model_dir + 'model_weights.hd5')

cPickle.dump(output, open(model_dir + 'model_history.pkl', 'wb'))
