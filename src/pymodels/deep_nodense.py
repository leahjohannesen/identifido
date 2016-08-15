from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D, AveragePooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.optimizers import SGD, Adam

def build_model(n_class):
    model_name = 'deep_padded_200'

    model = Sequential()
    model.add(Convolution2D(32, 3, 3, input_shape=(3,164,164)))
    model.add(ZeroPadding2D(padding=(1,1)))
    model.add(Activation('relu'))
    model.add(Convolution2D(32, 3, 3))
    model.add(ZeroPadding2D(padding=(1,1)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Convolution2D(64, 3, 3))
    model.add(ZeroPadding2D(padding=(1,1)))
    model.add(Activation('relu'))
    model.add(Convolution2D(128, 3, 3))
    model.add(ZeroPadding2D(padding=(1,1)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Convolution2D(256, 3, 3))
    model.add(ZeroPadding2D(padding=(1,1)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Convolution2D(512, 3, 3))
    model.add(ZeroPadding2D(padding=(1,1)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Convolution2D(1028, 3, 3))
    model.add(ZeroPadding2D(padding=(1,1)))
    model.add(Activation('relu'))

    model.add(AveragePooling2D(pool_size=(8,8)))
    model.add(Flatten())
    model.add(Dense(n_class))
    model.add(Activation('softmax'))
    
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy',
                  optimizer=sgd,
                  metrics=['accuracy']
                 )

    return model, model_name
