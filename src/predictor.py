import numpy as np
from keras.models import load_model
import sys
from scipy.ndimage import imread
from scipy.misc import imresize
import json

def predict(img):
    with open('/Users/lzkatz/Desktop/Galvanize/Capstone/Identifido/aux_files/dog_dict.json') as bd:
        classes = json.load(bd)
    print classes
    model_dir = '/Users/lzkatz/Desktop/Galvanize/Capstone/Identifido/model/basic/final_model.hdf5'
    model = load_model(model_dir)
    img_dim = model.input_shape[2]
    img_res = imresize(img, (img_dim, img_dim, 3))
    img_prep = np.array([img_res.T])
    
    class_pred = model.predict(img_prep)
    print class_pred
    sort_pred = np.argsort(class_pred.flatten())[:-6:-1]

    breed_pred = []
    for i in sort_pred:
        breed_pred.append((classes[i], class_pred[i]))
    
    return breed_pred

if __name__ == '__main__':
    pic_dir = '/Users/lzkatz/Desktop/Galvanize/Capstone/Identifido/data/test/'
    pic = sys.argv[1]
    img = imread(pic_dir + pic)
    results = predict(img)
    print results
