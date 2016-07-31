from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D
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
img_width, img_height = 198, 198

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

model = Sequential()
model.add(ZeroPadding2D((1,1), input_shape=(3,198,198)))
model.add(Convolution2D(64, 3, 3, activation='relu'))
model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(64, 3, 3, activation='relu'))
model.add(MaxPooling2D((2,2), strides=(2,2)))

model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(128, 3, 3, activation='relu'))
model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(128, 3, 3, activation='relu'))
model.add(MaxPooling2D((2,2), strides=(2,2)))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
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
