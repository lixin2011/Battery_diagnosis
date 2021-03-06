from tqdm import tqdm
from pandas import unique
from pandas import DataFrame
from time import sleep

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
            data_process = data.loc[data['batsn'] == sn,:]
            data_charge_count_diff = data_process['batchargecount'].diff(periods=1)
            for index in data_charge_count_diff.index:
                # 认为第一个值是不会发生跳变的
                # 会误删一个数据
                if (abs(data_charge_count_diff[index])) > 1:
                    error_index_list.append(index)
        print('\n充电次数跳变检查完成\n')
        print('\n充电次数跳变数据如下\n')
        for error_index in error_index_list:
            print(data.loc[error_index - 1:error_index + 2,:])
            # sleep(2)
        print('\n开始删除充电次数跳变数据\n')
        for error_index in tqdm(error_index_list):
            data = data.drop(error_index)
        print('\n充电次数跳变数据删除完成\n')
        return data

    if column_name == 'gmt_time':
        print('\n开始检查重采样数据\n')
        # 可以删除多个重采样的值，只保存一个
        error_index_list = []
        data['gmt_time_value'] = data['gmt_time'].apply(lambda x:x.value/(10**9))
        time_diff = data['gmt_time_value'].diff(periods=1)
        for index in tqdm(time_diff.index):
            if abs(time_diff[index]) < 1:
                error_index_list.append(index)
        print('\n数据重采样检查完成\n')
        print('\n重采样数据如下\n')
        for error_index in error_index_list:
            print(data.loc[error_index - 1:error_index,:])
            # sleep(2)
        print('\n开始删除重采样数据\n')
        for error_index in tqdm(error_index_list):
            data = data.drop(error_index)
        print('\n重采样数据删除完成\n')
        return data
    
def delete_vol_wave(data):
    '''
    删除电流为0，单体电压突变的点
    注意此处的index已经删除了一部分，不要使用iloc
    '''
    data['gmt_time_value'] = data['gmt_time'].apply(lambda x:x.value/(10**9))
    time_diff = data['gmt_time_value'].diff(periods=1)
    time_nodes = []
    print('\n开始划分时间块\n')
    for index in tqdm(time_diff.index):
        if time_diff[index] > 43200: # 间隔超过12个小时设置断点
            time_nodes.append(index)
    time_nodes = [0]+time_nodes+[-1]
    print('\n时间块划分完成\n')
    error_index = []
    error_mono = []
    print('\n开始检查单体电压跳变\n')
    for node_index in tqdm(range(len(time_nodes)-1)):
        # 进入一个时间块
        time_block = data.loc[time_nodes[node_index]:time_nodes[node_index+1],:]
        current_0_block = time_block.loc[time_block['batcurrent'] == 0,:]
        block_time_diff = current_0_block.loc[:,'gmt_time_value'].diff(periods=1)
        block_vol_tiff = current_0_block.loc[:,['bat_v1','bat_v2','bat_v3','bat_v4','bat_v5','bat_v6','bat_v7','bat_v8','bat_v9','bat_v10']].diff(periods=1)
        for index in current_0_block.index:
            # 进入一个电流均为0的块
            mono_time_diff = block_time_diff[index]
            for mono in ['bat_v1','bat_v2','bat_v3','bat_v4','bat_v5','bat_v6','bat_v7','bat_v8','bat_v9','bat_v10']:
                # 进入一个单体
                mono_vol_diff = block_vol_tiff.loc[index,mono]
                vol_change_per_sec = mono_vol_diff/mono_time_diff
                # 需要首先进行重采样检查，否则会出现除以0的情况
                # 每秒的电压变化值(mv/s)
                if abs(vol_change_per_sec) > 2:
                    error_mono.append(mono)
                    error_index.append(index)
                    # 如果多个单体都有问题，此处index可能会有重复，需要去重
    print('\n单体电压跳变检查完成\n')
    print('\n单体电压跳变数据如下\n')
    for mono,index in zip(error_mono,error_index):
        print(data.loc[index-1:index,['gmt_time',mono]])
        # sleep(2)
    print('\n开始删除单体电压跳变数据\n')
    error_index = list(set(error_index))
    for error_index in tqdm(error_index):
        data = data.drop(error_index)
    print('\n单体电压跳变数据删除完成\n')
    return data

def type_convert(data):
    data['batsn'] = data['batsn'].astype('object')
    data['battemp'] = data['battemp'].astype('float64')
    data['batcurrent'] = data['batcurrent'].astype('float64')
    data['batvoltage'] = data['batvoltage'].astype('float64')
    data['batsoc'] = data['batsoc'].astype('int64')
    data['batrscap'] = data['batrscap'].astype('float64')
    data['batafcap'] = data['batafcap'].astype('float64')
    data['batchargecount'] = data['batchargecount'].astype('int64')
    for name in ['bat_v1','bat_v2','bat_v3','bat_v4','bat_v5','bat_v6','bat_v7','bat_v8','bat_v9','bat_v10']:
        data[name] = data[name].astype('float64')
    data['gmt_time'] = data['gmt_time'].astype('datetime64')
    data['status'] = data['status'].astype('object')
    return data

    

