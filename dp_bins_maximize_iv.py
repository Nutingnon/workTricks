
# 动态规划分箱

import numpy as np
import pandas as pd


# def cal_iv(bins_dict, x_array, y_array):
#     for i in range(len(x_array)):
#         if x_array[i] in bins_dict:
#             if y_array[i] == 1:
#                 bins_dict[x_array[i]]["positive"] += 1
#             else:
#                 bins_dict[x_array[i]]["negative"] += 1
    
#     IV = 0
#     n_positive = sum(y_array == 1)
#     n_negative = len(y_array) - n_positive
#     for key in bins_dict:
#         p_pos = bins_dict[key]['positive']/n_positive
#         p_neg = bins_dict[key]['negative']/n_negative
#         woe_i = np.log(p_pos/p_neg)
#         iv_i = (p_pos-p_neg)*woe_i
#         IV += iv_i
        
#     return IV

# def iv_func(y,y_total_pos, y_total_neg):
#     iv = 0
#     n_positive = sum(y == 1)
#     n_negative = len(y) - n_positive
#     p_pos = n_positive/y_total_pos
#     p_neg = n_negative/y_total_neg
#     iv = (p_pos-p_neg)*np.log(p_pos/p_neg)
#     return iv

def iv_func2(unique_values,x_array,y):
    y_total_pos = sum(y==1)
    y_total_neg = len(y) - y_total_pos
    pos_cnt = 1
    neg_cnt = 1
    for i in range(len(x_array)):
        if x_array[i] in unique_values:
            if y[i]== 1:
                pos_cnt += 1
            else:
                neg_cnt += 1
                
    p_pos = pos_cnt/y_total_pos
    p_neg = neg_cnt/y_total_neg
    return (p_pos-p_neg)*np.log(p_pos/p_neg)
    

def dp_bins(x_array,y, n_bins=5):
    output_bin_result = dict()
    for i in range(n_bins):
        output_bin_result[str(i+1)] = []
    y_total_pos = sum(y==1)
    y_total_neg = len(y) - y_total_pos
    ############### INITIALIZATION for the dp #################
    ######## the element is [available_choices, max_iv] #######
    sorted_elements = sorted(list(set(x_array)))
    n_dim = len(sorted_elements)
    dp = dict()
    for row in range(n_bins):
        str_row = str(row)
        dp[str_row] = dict()
        for col in range(n_dim):
            subList = sorted_elements[col:]
            str_key = str(subList)
            dp[str_row].update({str_key: {"iv":-1, "subList":subList,"curr_best":[]}})
            if row ==0 and n_bins-(row+1) <= n_dim - len(subList):
                dp[str_row][str_key]["iv"] = iv_func2(subList, x_array, y)
                dp[str_row][str_key]["curr_best"]=[subList, ""]
    ################ INITIALIZATION DONE ######################
    ################ START ITERATION ##########################
            
            if row >= 1 and n_bins -(row+1) <= n_dim - len(subList):
                max_iv = -1
                previous_best = []
                curr_best = []
                for sub_idx in range(1,len(subList)):
                    curr_list = subList[:sub_idx]
                    post_list = subList[sub_idx:]
                    if dp[str(row-1)][str(post_list)]["iv"] != -1:
                        curr_iv = iv_func2(curr_list, x_array,y) + dp[str(row-1)][str(post_list)]["iv"]
                        if curr_iv>max_iv:
                            max_iv = curr_iv
                            previous_best = post_list
                            curr_best = curr_list
                            
                            
                            
                
                dp[str_row][str_key]["iv"] = max_iv
                dp[str_row][str_key]["curr_best"]=[curr_best,previous_best]
                
    # backtrack:
    output_bins = []
    max_iv = 0
    c_best =[]
    track_key = ""
    
    for key in dp[str(n_bins-1)]:
        iv_i = dp[str(row)][key]['iv']
        if iv_i>max_iv:
            max_iv = iv_i
            c_best = dp[str(row)][key]["curr_best"][0]
            track_key = str(dp[str(row)][key]["curr_best"][1])
    output_bins.append(c_best)
            
    
    for i in range(n_bins-2, -1, -1):
        print(i)
        output_bins.append(dp[str(i)][track_key]['curr_best'][0])
        track_key = str(dp[str(i)][track_key]["curr_best"][1])
        
    return dp, output_bins


a,b=dp_bins(np.asarray([1,2,3,4,1,1,7,8]), np.asarray([0,1,0,1,0,0,1,0]), n_bins=3)