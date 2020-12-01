import pandas as pd
import os

def delete_na(data):
    '''
    删除含有nan值的行数据
    '''
    droped_data = data.dropna(axis=0,how='any')
    return droped_data 

def delete_value_0(data,column_name):
    '''
    删除指定列含有0的数据
    '''
    data_deleted_0 = data.drop(data[(data[column_name] == 0)].index)
    return data_deleted_0

def delete_difference_irrational(data,column_name):
    '''
    删除指定列指定差值的数据
    '''
    if column_name == 'batchargecount':
        data_diff = data[column_name].diff(periods=1)
        data_deleted_difference = data.drop(data[(data_diff > 1)|(data_diff < -1)].index)
    if column_name == 'gmt_time':
        data['gmt_time'] = pd.to_datetime(data.gmt_time)
        data['time_value'] = data['gmt_time'].apply(lambda x: int((x.value)/10**9))
        data_diff = data['time_value'].diff(periods=-1)
        data_deleted_difference = data.drop(data[(data_diff < 5)&(data_diff > -5)].index)   
    return data_deleted_difference

def delete_vol_wave(data):
    '''
    删除电流为0，单体电压突变的点
    '''
    data.loc[:,'time_value'] = data.loc[:,'gmt_time'].apply(lambda x: int((x.value)/10**9))
    # 计算出采样间隔，按照时间连续分块
    time_diff = data.loc[:,'time_value'].diff(periods=1)
    time_node = list(time_diff[(time_diff > 3600)|(time_diff < -3600)].index)
    time_nodes = [0] + time_node + [-1]
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
    return data