from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.optimizers import SGD, Adam

def build_model(n_class):
    model_name = 'ensemble_onehidden'

    model = Sequential()
    model.add(Dense(n_class, input_dim=392))
    model.add(Activation('softmax'))
    
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy',
                  optimizer=sgd,
                  metrics=['accuracy']
                 )

    return model, model_name
