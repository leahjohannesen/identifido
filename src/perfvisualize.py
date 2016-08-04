import globes as G
import seaborn as sbn
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import json

def get_breed_labels(arr, bd):
    idx_list = []
    for val in arr:
        idx_list.append(bd[str(val)])
    return idx_list
        
def cat_acc(path):
    with open('./aux_files/breed_dict.json') as bd:
        breed_dict = json.load(bd)

    f, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3,2)
    df = pd.read_csv(path, index_col=0, header=None)
    df.columns = ['act', 'pred']
    df['right'] = df['pred'] == df['act']

    total_by_class = df.groupby('act').count()
    n_tot = total_by_class['pred'].values
    n_show = 20

    
    #number of correct
    pred_right_df = df.groupby('act').sum()
    right_arr = pred_right_df['right'].values 
    right_per_arr = right_arr / n_tot
    y_sorted = np.sort(right_per_arr)[::-1]
    x_sorted = np.argsort(right_per_arr)[::-1]
    
    ##hist of accuracies
    sbn.distplot(right_per_arr, kde=False, ax=ax1, bins=25)

    ##total number of pictures
    y_tot = np.sort(n_tot)[:-n_show:-1]
    x_tot = np.argsort(n_tot)[:-n_show:-1]
    x_tot_lst = get_breed_labels(x_tot, breed_dict)
    sbn.barplot(x_tot_lst, y_tot, ax=ax2, order=x_tot_lst)

    ##top/bot 10
    x_top = x_sorted[:n_show]
    x_bot = x_sorted[-n_show:]
    y_top = y_sorted[:n_show]
    y_bot = y_sorted[-n_show:]
    sbn.barplot(x_top, y_top, ax=ax3, order=x_top)
    sbn.barplot(x_bot, y_bot, ax=ax4, order=x_bot)
    
    ##most predicted/number
    num_pred_df = df.groupby('pred').count()
    pred_arr = num_pred_df['right'].values
    pred_per_arr = pred_arr / n_tot
    y_pred_sorted = np.sort(pred_per_arr)[::-1]
    x_pred_sorted = np.argsort(pred_per_arr)[::-1]
    
    #top/bot pred 10
    x_num_top = x_pred_sorted[:n_show]
    x_num_bot = x_pred_sorted[-n_show:]
    y_num_top = y_pred_sorted[:n_show]
    y_num_bot = y_pred_sorted[-n_show:]
    sbn.barplot(x_num_top, y_num_top, ax=ax5, order=x_num_top)
    sbn.barplot(x_num_bot, y_num_bot, ax=ax6, order=x_num_bot)

    for ax in f.axes:
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    plt.show()

if __name__ == '__main__':
    test_or_all = sys.argv[1]
    temp_or_final = sys.argv[2]
    model_name = sys.argv[3]

    csv_path = './model/' + model_name + '/' + test_or_all + '_' + temp_or_final + '.csv'
    cat_acc(csv_path)   
