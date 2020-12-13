from pandas import unique,concat
from pandas import DataFrame

def get_statistic_data(data):
    '''
    按照电池编号进行信息统计
    '''
    statistic_data = DataFrame()
    sn_list = list(unique(data.loc[:,'batsn']))
    for sn,index in zip(sn_list,range(len(sn_list))):
        data_process = data.loc[data['batsn'] == sn,:]
        statistic_data.loc[index,'sn'] = sn
        statistic_data.loc[index,'max_temp'] = data_process['battemp'].max()
        statistic_data.loc[index,'min_temp'] = data_process['battemp'].min()
        statistic_data.loc[index,'max_vol'] = data_process['batvoltage'].max()
        statistic_data.loc[index,'min_vol'] = data_process['batvoltage'].min()
        statistic_data.loc[index,'max_cur'] = data_process['batcurrent'].max()
        statistic_data.loc[index,'min_cur'] = data_process['batcurrent'].min()
    return statistic_data

def check_border(data,charge_vol_threshold,discharge_vol_threshold,cur_threshold,temp_threshold):
    '''
    按照给定边界，返回异常数据及其统计
    '''
    boder_check_frequency = DataFrame()
    overcharge_data = DataFrame()
    overdischarge_data = DataFrame()
    sn_list = list(unique(data.loc[:,'batsn']))
    for sn,index in zip(sn_list,range(len(sn_list))):
        # 进入一块电池
        data_process = data.loc[data['batsn'] == sn,:]
        boder_check_frequency.loc[index,'sn'] = sn
        for mono in ['bat_v1','bat_v2','bat_v3','bat_v4','bat_v5','bat_v6','bat_v7','bat_v8','bat_v9','bat_v10']:
            overcharge_data = concat([overcharge_data,data_process.loc[(data[mono] > charge_vol_threshold)&(data_process['status'] == '充电'),:]])
            overdischarge_data = concat([overdischarge_data,data_process.loc[(data[mono] < discharge_vol_threshold)&(data_process['status'] == '放电'),:]])
        overcharge_data = overcharge_data.drop_duplicates(keep='first')  
        boder_check_frequency.loc[index,'overcharge'] = len(overcharge_data)
        overdischarge_data = overdischarge_data.drop_duplicates(keep='first')
        boder_check_frequency.loc[index,'overdischarge'] = len(overdischarge_data)
        over_cur_data = data_process.loc[data['batcurrent'] > cur_threshold,:]
        boder_check_frequency.loc[index,'overcurrent'] = len(over_cur_data)
        over_temp_data = data_process.loc[data['battemp'] > temp_threshold,:]
        boder_check_frequency.loc[index,'overtemp'] = len(over_temp_data)
    return boder_check_frequency,overcharge_data,overdischarge_data,over_cur_data,over_temp_data




