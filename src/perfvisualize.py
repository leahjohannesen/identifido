import globes as G
import seaborn as sbn
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys

def cat_acc(path):
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)
    df = pd.read_csv(path, header=None)
    df.columns = ['act', 'pred']
    df['right'] = df['pred'] == df['act']

    total_by_class = df.groupby('act').count()
    n_tot = total_by_class['pred'].values
    n_show = 1

    #number of correct
    pred_right_df = df.groupby('act').sum()
    right_arr = pred_right_df['right'].values 
    right_per_arr = right_arr / n_tot
    y_sorted = np.sort(right_per_arr)[::-1]
    x_sorted = np.argsort(right_per_arr)[::-1]
    
    ##hist of accuracies
    sbn.distplot(right_per_arr, kde=False, ax=ax1)

    ##top/bot 10
    x_top = np.append(x_sorted[:n_show], x_sorted[-n_show:])
    y_top = np.append(y_sorted[:n_show], y_sorted[-n_show:])
    sbn.barplot(x_top, y_top, ax=ax2)
    
    ##most predicted/number
    num_pred_df = df.groupby('pred').count()
    pred_arr = num_pred_df['right'].values
    pred_per_arr = pred_arr / n_tot
    y_pred_sorted = np.sort(pred_per_arr)[::-1]
    x_pred_sorted = np.argsort(pred_per_arr)[::-1]
    
    #top/bot pred 10
    x_num = np.append(x_pred_sorted[:n_show], x_pred_sorted[-n_show:])
    y_num = np.append(y_pred_sorted[:n_show], y_pred_sorted[-n_show:])
    sbn.barplot(x_num, y_num, ax=ax3)

    plt.show()

if __name__ == '__main__':
    model_name = sys.argv[2]
    test_or_all = sys.argv[1]

    #csv_path = G.MOD + model_name + '/' + test_or_all + '.csv'
    csv_path = './data/test.csv'
    cat_acc(csv_path)   
