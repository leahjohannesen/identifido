from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.optimizers import SGD


# dimensions of our images.
img_width, img_height = 200, 200

train_data_dir = 'train'
test_data_dir = 'test'
nb_epoch = 50

# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
        rescale=1./255,
        fill_mode='constant',
        horizontal_flip=True)

test_datagen = ImageDataGenerator(
        rescale=1./255,
        fill_mode='constant')

train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        # save_to_dir=out_train_dir,
        batch_size=100
        )

test_generator = test_datagen.flow_from_directory(
        test_data_dir,
        target_size=(img_width, img_height),
        # save_to_dir=out_test_dir,
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

# this is the augmentation configuration we will use for training

model.fit_generator(
        train_generator,
        samples_per_epoch=train_generator.N,
        nb_epoch=nb_epoch,
        validation_data=test_generator,
        nb_val_samples=test_generator.N)
