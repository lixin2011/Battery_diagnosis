import pandas as pd
import os
from tqdm import tqdm
from pandas import unique
import time as ti

def delete_na(data):
    '''
    删除含有nan值的行数据
    '''
    print('\n开始检查缺失值\n')
    with tqdm(total=100) as pbar:
        pbar.update(0)
        result = data.isnull().sum()
        pbar.update(100)
    print('\n缺失值检查完成\n')
    print('\n每列对应的缺失数据如下：\n')
    print(result)
    print('\n开始删除缺失值\n')
    with tqdm(total=100) as pbar:
        pbar.update(0)
        data_droped = data.dropna(axis=0,how='any')
        pbar.update(100)
    print('\n缺失值删除完成')
    return data_droped 

def delete_value_0(data,column_name):
    '''
    删除指定列含有0的数据
    '''
    print('\n')
    print('\n开始检查'+column_name+'列含0数据\n')
    with tqdm(total=100) as pbar:
        pbar.update(0)
        result = data.loc[(data[column_name] == 0),:]
        pbar.update(100)
    print('\n'+column_name+'列含0数据检查完成\n')
    print(column_name+'列为0的行数据如下：\n')
    print(result)
    print('\n开始清删除含0数据\n')
    with tqdm(total=100) as pbar:
        pbar.update(0)
        data_deleted_0 = data.drop(data[(data[column_name] == 0)].index)
        pbar.update(100)
    print('\n含0数据删除完成')
    return data_deleted_0

def delete_difference_irrational(data,column_name):
    '''
    删除指定列指定差值的数据
    作差的数据均采用遍历补值的形式，整体求差易删错值
    需要在时间块内操作
    '''
    if column_name == 'batchargecount':
        print('\n开始检查充电次数跳变\n')
        # 只能解决跳变一个值的数据 
        error_index_list = []
        sn = data.loc[:,'batsn']
        sn_list = list(unique(sn))
        # 在单个序列号块内操作
        for sn in tqdm(sn_list):   
            data_process = pd.DataFrame()
            data_process['count'] = data.loc[data['batsn'] == sn,'batchargecount'].values
            data_charge_count_diff = data_process.diff(periods=1)
            print(data_charge_count_diff)
            for index in data_charge_count_diff.index:
                # 认为第一个值是不会发生跳变的
                # 会误删一个数据
                if (abs(data_charge_count_diff.loc[index,'count'])) > 2:
                    print(abs(data_charge_count_diff.loc[index,'count']))
                    error_index_list.append(index)
        print('\n充电次数跳变检查完成\n')
        print('\n充电次数跳变数据如下\n')
        for error_index in error_index_list:
            print(data.iloc[error_index - 2:error_index + 3,:])
            ti.sleep(2)
        print('\n开始删除充电次数跳变数据\n')
        for error_index in tqdm(error_index_list):
            print(data.iloc[[error_index],:])
            data_deleted_difference = data.drop(data.iloc[[error_index],:].index)
        print('\n充电次数跳变数据删除完成\n')
        return data_deleted_difference

    if column_name == 'gmt_time':
        print('\n开始检查重采样数据\n')
        # 可以删除多个重采样的值，只保存一个
        time = pd.DataFrame(data.index.values,columns=['time'])
        time['time'] = time['time'].apply(lambda x:x.value/(10**9))
        time_diff = time.diff(periods=1)
        error_index_list = []
        for index in tqdm(time_diff.index):
            if abs(time_diff.loc[index,'time']) < 1:
                error_index_list.append(index)
        print('\n数据重采样检查完成\n')
        print('\n重采样数据如下\n')
        for error_index in error_index_list:
            print(data.iloc[error_index - 2:error_index + 2,:])
            ti.sleep(2)
        print('\n开始删除重采样数据\n')
        for error_index in tqdm(error_index_list):
            data_deleted_difference = data.drop(data.iloc[[error_index],:].index)
        print('\n重采样数据删除完成\n')
        return data_deleted_difference
    '''
def delete_vol_wave(data):
    '''
    '删除电流为0，单体电压突变的点'
    
    '''
    time = pd.DataFrame(data.index.values,columns=['time'])
    time['time'] = time['time'].apply(lambda x:x.value/(10**9))
    time_diff = time.diff(periods=1)
    time_nodes = []
    print('\n开始划分时间块\n')
    for index in tqdm(time_diff.index):
        if time_diff.loc[index,'time'] > 43200:
            time_nodes.append(index)
    time_nodes = [0]+time_nodes+[-1]
    print('\n时间块划分完成\n')
    print(time_nodes)
    for node_index in tqdm(range(len(time_nodes)-1)):
    

    #在单个时间块进行操作
    for i in range(len(time_nodes) - 1):
        time_block = data.iloc[time_nodes[i]:time_nodes[i+1],:]
        current_block = time_block[time_block['batcurrent'] == 0]
        time_diff = current_block.loc[:,'time_value'].diff(periods=1)
        # 在时间块内，电流为0处进行操作
        index = list(current_block.index)
        # 在每个单体内进行分析
        delete_list = []
        for mono in ['bat_v1','bat_v2','bat_v3','bat_v4','bat_v5','bat_v6','bat_v7','bat_v8','bat_v9','bat_v10']:
            for i in range(len(index) - 1): # 操作元素为i+1
                vol_diff = current_block.loc[index[i+1],mono] - current_block.loc[index[i],mono]
                rate_dec = vol_diff/time_diff[index[i+1]]*3600/1000   # 每小时单体压降,上限值0.8（v）
                if (rate_dec > (1))|(rate_dec < (-1)):
                    current_block.loc[index[i+1],mono] = current_block.loc[index[i],mono]   #直接使用原值
                    delete_list.append(index[i+1])
                    print('索引：',index[i+1],end='  ')
                    print('单体：',mono)
                    print('每小时单体电压变化：{:.2f}'.format(rate_dec))
                    # 更新值后重新计算
        if delete_list:
            for index in set(delete_list):
                data.drop(index=index,inplace=True)
    return data'''