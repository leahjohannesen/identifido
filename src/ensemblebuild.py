import globes as G 
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint
import json
import h5py
import os
import sys
import numpy as np

sys.path.append(G.NET)
model_filename = sys.argv[1]

if len(model_filename) > 0:
    mod = __import__(model_filename)

# parameters
nb_epoch = 100 

# read ensemble data
x_trn = np.load(G.AUX + 'ens_x_trn.npy')
x_val = np.load(G.AUX + 'ens_x_val.npy')
y_trn = np.load(G.AUX + 'ens_y_trn.npy')
y_val = np.load(G.AUX + 'ens_y_val.npy')


model, model_name = mod.build_model(98)

# saves the output in the model_dir
model_dir = G.MOD + model_name + '/'
os.mkdir(model_dir)
temp_path = model_dir + 'temp_model.hdf5'

#update the model if stuff gets better
checkpointer = ModelCheckpoint(filepath=temp_path, verbose=1, save_best_only=True)

# this actually fits the model
output = model.fit(
        	x=x_trn, y=y_trn,
                batch_size=32,
        	nb_epoch=nb_epoch,
        	validation_data=(x_val, y_val),
                callbacks=[checkpointer])

model.save(model_dir + 'final_model.hdf5')

hist = output.history
params = output.params

with open(model_dir + 'history.json', 'wb') as h:
    json.dump(hist, h)
with open(model_dir + 'params.json', 'wb') as p:
    json.dump(params, p)
