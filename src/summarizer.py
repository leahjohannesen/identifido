from keras.models import load_model
import matplotlib.pyplot as plt
import seaborn as sbn
import sys
import json
import numpy as np

def get_history():
    with open(model_dir + 'history.json', 'r') as h:
        return json.load(h)

def get_param():
    with open(model_dir + 'params.json', 'r') as p:
        return json.load(p) 

def acc_graph(history, ax):
    train_acc = np.array(history['acc'])
    val_acc = np.array(history['val_acc'])
    sbn.set_style('darkgrid')
    ax.plot(train_acc, label='Train')
    ax.plot(val_acc, label='Val')
    ax.set_title('Model accuracy')
    ax.legend(loc=4)

def loss_graph(history, ax):
    train_loss = np.array(history['loss'])
    val_loss = np.array(history['val_loss'])
    sbn.set_style('darkgrid')
    ax.plot(train_loss, label='Train')
    ax.plot(val_loss, label='Val')
    ax.set_title('Model loss')
    ax.legend()

if __name__ == "__main__":
    home_dir = '/Users/lzkatz/Desktop/Galvanize/Capstone/Identifido/'
    dir_name = sys.argv[1]

    model_dir = home_dir + 'model/' +  dir_name + '/'
    model = load_model(model_dir + 'final_model.hd5')

    model_hist = get_history()
    model_param = get_param()

    model.summary()

    f, (ax1, ax2) = plt.subplots(2,1)

    acc_graph(model_hist, ax1)
    loss_graph(model_hist, ax2)
    plt.show()
