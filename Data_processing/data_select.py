from pandas import DataFrame
from pandas import unique,concat
from tqdm import tqdm

def get_sn(data):
    '''
    输入数据，返回数据中存在的sn
    '''
    sn = data.loc[:,'batsn']
    sn_unique = unique(sn)
    return sn_unique

def select_sn(data,sn_list):
    '''
    输入数据及编号列表，返回给定电池编号列表的对应数据
    '''
    print('\n')
    if sn_list:
        data_sn = DataFrame(columns=data.columns)
        for sn in tqdm(sn_list):
            data_sn = concat([data.loc[data.loc[:,'batsn'] == sn,:],data_sn])
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
    sta_unique = unique(sta)
    return sta_unique

def select_state(data,state_list):
    '''
    输入数据及状态列表，返回状态列表对应的数据
    '''
    print('\n')
    if state_list:
        data_state = DataFrame(columns=data.columns)
        for state in tqdm(state_list):
            data_state = concat([data.loc[data.loc[:,'status'] == state,:],data_state])
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
    index_or = data.index
    data.index = data.loc[:,'gmt_time']
    # 使用时间项作为索引，可以更好的控制索引
    if (time_start != '')&(time_end != ''):
        data_time = data.loc[time_start:time_end,:]
    elif (time_start == '')&(time_end != ''):
        data_time = data.loc[:time_end,:]
    elif (time_start != '')&(time_end == ''):
        data_time = data.loc[time_start:,:]
    else:
        data_time = data
    data_time.index = index_or
    print(data_time)
    return data_time