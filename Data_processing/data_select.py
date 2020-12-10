import pandas as pd
import os
import tqdm

def get_sn(data):
    '''
    输入数据，返回数据中存在的sn
    '''
    sn = data.iloc[:,0]
    sn_unique = list(pd.unique(sn))
    return sn_unique

def select_sn(data,sn_list):
    '''
    输入数据及编号列表，返回给定电池编号列表的对应数据
    '''
    print('\n')
    if sn_list:
        data_sn = pd.DataFrame(columns=data.columns)
        for sn in tqdm.tqdm(sn_list):
            data_sn = pd.concat([data.loc[data.loc[:,'batsn'] == sn,:],data_sn])
    else:
        data_sn = data
    print('\n')
    print(data_sn)
    return data_sn

def get_state(data):
    '''
    输入数据，返回数据中存在的state
    '''
    sta = data.loc[:,'status']
    sta_unique = pd.unique(sta)
    return sta_unique

def select_state(data,state_list):
    '''
    输入数据及状态列表，返回状态列表对应的数据
    '''
    print('\n')
    if state_list:
        data_state = pd.DataFrame(columns=data.columns)
        for state in tqdm.tqdm(state_list):
            data_state = pd.concat([data.loc[data.loc[:,'status'] == state,:],data_state])
    else:
        data_state = data
    print('\n')
    print(data_state)
    return data_state

def select_time(data,time_start,time_end):
    '''
    输入数据和起始，结束时间，返回给定时间段对应数据
    输入可以一侧为空或全部为空，表示不做时间点限制
    '''
    print(time_start)
    if (time_start != '')&(time_end != ''):
        data_time = data.loc[time_start:time_end,:]
    elif (time_start == '')&(time_end != ''):
        data_time = data.loc[:time_end,:]
    elif (time_start != '')&(time_end == ''):
        data_time = data.loc[time_start:,:]
    else:
        data_time = data
    print(data_time)
    return data_time