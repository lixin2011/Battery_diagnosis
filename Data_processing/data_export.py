
def export_temp(data):
    '''
    导出数据的温度项
    '''
    temp = data.loc[:,'battemp']
    return temp

def export_cur(data):
    '''
    导出数据的电流项
    '''
    cur = data.loc[:,'batcurrent']
    return cur

def export_vol_total(data):
    '''
    导出数据的总电压项
    '''
    vol = data.loc[:,'batvoltage']
    return vol

def export_vol_mono(data):
    '''
    导出数据的单体电压项
    '''
    vol_mono = data.loc[:,['bat_v1','bat_v2','bat_v3','bat_v4','bat_v5','bat_v6','bat_v7','bat_v8','bat_v9','bat_v10']]  
    return vol_mono

def export_cap_total(data):
    '''
    导出数据的总容量项
    '''
    cap = data.loc[:,'batafcap']           
    return cap

def export_cap_now(data):
    '''
    导出数据的当前容量项
    '''
    cap_now = data.loc[:,'batrscap']
    return cap_now

def export_soc(data):
    '''
    导出数据的当前容量项
    '''
    soc = data.loc[:,'batrsoc']
    return soc

def export_charge_count(data):
    '''
    导出数据的充电次数
    '''
    charge_count = data.loc[:,'batchargecount']
    return charge_count  
