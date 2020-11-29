import pandas as pd
import os

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