from pandas import isna
from pandas import DataFrame
from tqdm import tqdm 

def get_sampling_rate(data):
    '''
    输入数据，返回采样间隔构成的字典
    '''
    time = DataFrame(data.index)
    time['gmt_time'] = time['gmt_time'].apply(lambda x:x.value/(10**9))
    diff = time.diff(periods=1)
    diff_mean =diff['gmt_time'].mean()
    diff_max = diff['gmt_time'].max()
    diff_min = diff['gmt_time'].min()
    data_diff_max_index = diff.loc[diff['gmt_time'] == diff_max,:].index.tolist()
    data_diff_max = data.iloc[(data_diff_max_index[0] - 2):(data_diff_max_index[0] + 2),]
    data_diff_min_index = diff.loc[diff['gmt_time'] == diff_min,:].index.tolist()
    data_diff_min = data.iloc[(data_diff_min_index[0] - 2):(data_diff_min_index[0] + 2),]
    return {'最小采样间隔':diff_min,'最大采样间隔':diff_max,'平均采样间隔':diff_mean},data_diff_min,data_diff_max

def get_data_validity(data):
    '''
    检查有效数据占比
    '''
    total_data_number = data.shape[0]
    check_frame = DataFrame()
    print('\n')
    print('检查温度为-273以及空值\n')
    check_frame['temp_check'] = data['battemp'] == -273 | (isna(data['batrsoc']))
    print('检查电流为空值\n')
    check_frame['current_check'] = (isna(data['batcurrent']))
    print('检查电压为空值\n')
    check_frame['voltage_check'] = (isna(data['batcurrent']))
    print('检查soc为0及空值\n')
    check_frame['soc_check'] = (data['batrsoc'] == 0) | (isna(data['batrsoc']))
    print('检查单体电压为0及空值\n')
    for vol in tqdm(['v1','v2','v3','v4','v5','v6','v7','v8','v9','v10']):
        check_frame[vol+'_check'] = (data['bat_'+vol] == 0) | (isna(data['bat_'+vol]))
    print('\n')
    check_frame['numbers_check'] = check_frame.sum(axis=1)
    check_frame['results_check'] = check_frame['numbers_check'] != 0
    invalid_data_number = check_frame['results_check'].sum()
    valid_data_number = total_data_number - invalid_data_number
    valid_data = data.loc[check_frame['results_check'] == 0,:]
    invalid_data = data.loc[check_frame['results_check'] != 0,:]
    return {'有效数据量':valid_data_number,'无效数据量':invalid_data_number,'总数据量':total_data_number},valid_data,invalid_data



