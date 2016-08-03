import numpy as np
from keras.models import load_model
import sys
from scipy.ndimage import imread
from scipy.misc import imresize

def predict(img):
    model_dir = '/Users/lzkatz/Desktop/Galvanize/Capstone/Identifido/model/basic/final_model.hdf5'
    model = load_model(model_dir)
    img = img.resize


if __name__ == '__main__':
    pic_dir = '/Users/lzkatz/Desktop/Galvanize/Capstone/Identifido/data/test/'
    model 
    pic = sys.argv[1]
    img = imread(pic_dir + pic)
    results = predict(img)
