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
    
    #bunch of figures
    fig1, ax1 = plt.subplots(1,1)
    fig2, ax2 = plt.subplots(1,1)
    fig3, (ax31, ax32) = plt.subplots(2,1, sharex=True)
    fig4, (ax41, ax42) = plt.subplots(2,1, sharex=True)

    df = pd.read_csv(path, index_col=0, header=None)
    df.columns = ['act', 'pred']
    df['right'] = df['pred'] == df['act']

    total_by_class = df.groupby('act').count()
    n_tot = total_by_class['pred'].values
    n_tot = n_tot.astype(float)
    n_show = len(n_tot)
    x_master = np.array(range(n_show))
    x_master_lab = get_breed_labels(x_master, breed_dict)

    
    #number of correct
    pred_right_df = df.groupby('act').sum()
    right_arr = pred_right_df['right'].values 
    right_per_arr = right_arr / n_tot
    
    ##hist of accuracies
    sbn.distplot(right_per_arr, kde=False, ax=ax1, bins=25)

    ##total number of pictures
    x_tot_sort = np.argsort(n_tot)[::-1]
    x_tot_sort_lst = get_breed_labels(x_tot_sort, breed_dict)
    sbn.barplot(x_master_lab, n_tot, ax=ax2, order=x_tot_sort_lst)

    ##top/bot 10
    x_acc_sort = np.argsort(right_per_arr)[::-1]
    x_acc_sort_lab = get_breed_labels(x_acc_sort, breed_dict)
    sbn.barplot(x_master_lab, right_per_arr, ax=ax31, order=x_acc_sort_lab)
    sbn.barplot(x_master_lab, n_tot, ax=ax32, order=x_acc_sort_lab)
    
    ##most predicted/number
    num_pred_df = df.groupby('pred').count()
    pred_arr = num_pred_df['right'].values
    pred_per_arr = pred_arr / n_tot
    
    #top/bot pred 10
    x_pred_sort = np.argsort(pred_per_arr)[::-1]
    x_pred_sort_lab = get_breed_labels(x_pred_sort, breed_dict)
    sbn.barplot(x_master_lab, pred_per_arr, ax=ax41, order=x_pred_sort_lab)
    sbn.barplot(x_master_lab, n_tot, ax=ax42, order=x_pred_sort_lab)

    ax1.set_title('Histogram of Accuracies')
    ax2.set_title('# of Pics per Breed')
    ax31.set_title('% Accuracy per Class')
    ax41.set_title('% Class Predicted per Class')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90)
    ax32.set_xticklabels(ax32.get_xticklabels(), rotation=90)
    ax42.set_xticklabels(ax42.get_xticklabels(), rotation=90)
    fig3.subplots_adjust(hspace=0)
    fig4.subplots_adjust(hspace=0)
    fig3.tight_layout()
    fig4.tight_layout()
    plt.show()

if __name__ == '__main__':
    trn_val_tst_all = sys.argv[1]
    temp_or_final = sys.argv[2]
    model_name = sys.argv[3]

    csv_path = './model/' + model_name + '/' + trn_val_tst_all + '_' + temp_or_final + '.csv'
    cat_acc(csv_path)   
