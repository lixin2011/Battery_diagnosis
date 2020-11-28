# -*- coding: utf-8 -*-
import pandas as pd
import os


def get_path(): 
    '''
    返回电池数据文件具体路径
    '''
    # 创建工作目录，放置文件
    print('\n********************   程序的工作目录为D:\qixiang，请注意查看   ********************')
    try:
        os.mkdir(r'D:\qixiang')
        print('\n********************   目录D:\qixiang已创建   ********************')
    except FileExistsError:
        print('\n********************   目录D:\qixiang已存在   ********************')
    
    input('\n请在目录D:\qixiang放入单个电池数据文件(支持csv和xlsx文件，按回车继续)')
    # 选择文件
    os.chdir(r'D:\qixiang')  
    file_list = os.listdir(r'D:\qixiang')
    print('\n检测到的电池文件为：',file_list)
    file_path = 'D:\\qixiang\\' + file_list[0]
    return file_path

def get_data(path):
    '''
    输入文件路径，读取并返回所有电池数据
    '''
    file_type = path.split('.')[-1]
    print('\n********************   数据读取中，请稍候   ********************')
    if file_type == 'xlsx':
        data_all = pd.read_excel(path)
    elif file_type == 'csv':
        data_all = pd.read_csv(path,encoding='gbk')
    print('\n********************   数据读取完成   ********************')
    return data_all

def get_sn(data):
    '''
    输入数据，返回数据中存在的sn
    '''
    sn = data.iloc[:,0]
    sn_unique = list(pd.unique(sn))
    return sn_unique

def select_sn(data,sn):
    '''
    输入数据及编号，返回给定电池编号对应数据
    '''
    data_sn = data.loc[data.iloc[:,0] == sn,:]
    return data_sn

def get_state(data):
    '''
    输入数据，返回数据中存在的state
    '''
    sta = data.loc[:,'status']
    sta_unique = pd.unique(sta)
    return sta_unique

def select_state(data,state):
    '''
    输入数据及状态，返回对应的数据
    '''
    data_state = data.loc[data.status == state,:]
    return data_state

def select_time(data,time_start,time_end):
    '''
    输入数据和起始，结束时间，返回给定时间段对应数据
    '''
    # 新增一列，将时间数据转换为自然数
        #  表示time的列是否需要用户输入
    # for i in range(len(data.loc[:,'gmt_time'])):
        # data.loc[i,'time_value'] = data.loc[i,'gmt_time'].value
    data['time_value'] = data['gmt_time'].apply(lambda x: x.value)
    for i in range(len(time_start)):
        time_start[i] = int(time_start[i])
    # 将输入转化为时间戳
    time_start = pd.Timestamp(time_start[0],time_start[1],time_start[2],time_start[3],time_start[4],time_start[5])
    time_start_value = time_start.value
    for i in range(len(time_end)):
        time_end[i] = int(time_end[i])
    time_end = pd.Timestamp(time_end[0],time_end[1],time_end[2],time_end[3],time_end[4],time_end[5])
    time_end_value = time_end.value
    data_time = data.loc[(data.time_value>=time_start_value)&(data.time_value<=time_end_value),:]
    data_time = data_time.drop(columns=['time_value'])
    return data_time


def export_temp(data):
    '''
    导出数据的温度项
    '''
    temp = data[['gmt_time','battemp']]
    return temp

def export_cur(data):
    '''
    导出数据的电流项
    '''
    cur = data[['gmt_time','batcurrent']] 
    return cur

def export_vol_total(data):
    '''
    导出数据的总电压项
    '''
    vol = data[['gmt_time','batvoltage']]
    return vol

def export_vol_mono(data):
    '''
    导出数据的单体电压项
    '''
    vol_mono = data[[18,8,9,10,11,12,13,14,15,16,17]]  
    return vol_mono

def export_cap_total(data):
    '''
    导出数据的总容量项
    '''
    cap = data[['gmt_time','batafcap']]           
    return cap

def export_cap_now(data):
    '''
    导出数据的当前容量项
    '''
    cap_now = data[['gmt_time','batrscap']]  
    return cap_now

def export_soc(data):
    '''
    导出数据的当前容量项
    '''
    soc = data[['gmt_time','batrsoc']]  
    return soc

def export_charge_count(data):
    '''
    导出数据的充电次数
    '''
    charge_count = data[['gmt_time','batchargecount']]
    return charge_count  


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





