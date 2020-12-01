from datetime import datetime
import pandas as pd
import json
import requests
import numpy as np

def download_json_data(url):
    '''
    返回json数据的生成器，一次一行
    '''
    r = requests.get(url,stream=True)
    for line in r.iter_lines():
        if line:
            print('----downloading----')
            print(line)
            yield json.loads(line)
        
def convert_to_dataframe(data):
    '''
    对json数据进行索引，返回一个（1，39）的dataframe
    '''
    data_block = np.array([data['info']['devcode'],data['info']['receiveTime'],data['ffBatteryStatus']['rssi'],data['ffBatteryStatus']['errorLevel'],data['ffBatteryStatus']['errorCode']
        ,data['ffBatteryStatus']['current'],data['ffBatteryStatus']['voltageInner'],data['ffBatteryStatus']['blueConnectState'],data['ffBatteryStatus']['chargeState'],data['ffBatteryStatus']['heatState']
        ,data['ffBatteryStatus']['soc'],data['ffBatteryStatus']['soh'],data['ffBatteryStatus']['cellVolBalance'],data['ffBatteryStatus']['cellVoltageList'][0],data['ffBatteryStatus']['cellVoltageList'][1],data['ffBatteryStatus']['cellVoltageList'][2]
        ,data['ffBatteryStatus']['cellVoltageList'][3],data['ffBatteryStatus']['cellVoltageList'][4],data['ffBatteryStatus']['cellVoltageList'][5],data['ffBatteryStatus']['cellVoltageList'][6]
        ,data['ffBatteryStatus']['cellVoltageList'][7],data['ffBatteryStatus']['cellVoltageList'][8],data['ffBatteryStatus']['cellVoltageList'][9],data['ffBatteryStatus']['cellVoltageList'][10]
        ,data['ffBatteryStatus']['cellVoltageList'][11],data['ffBatteryStatus']['cellVoltageList'][12],data['ffBatteryStatus']['cellVoltageList'][13],data['ffBatteryStatus']['cellVoltageList'][14]
        ,data['ffBatteryStatus']['cellVoltageList'][15],data['ffBatteryStatus']['cellVoltageList'][16],data['ffBatteryStatus']['cellTempList'][0],data['ffBatteryStatus']['cellTempList'][1],data['ffBatteryStatus']['cellTempList'][2]
        ,data['ffBatteryStatus']['cellTempList'][3],data['ffBatteryStatus']['otherTempList'][0],data['ffBatteryStatus']['otherTempList'][1],data['ffBatteryStatus']['otherTempList'][2]
        ,data['ffBatteryStatus']['otherTempList'][3],data['ffBatteryStatus']['otherTempList'][4]]).reshape(1,39)
    df = pd.DataFrame(
        columns=['编号','时间戳','GSM信号','故障等级','故障代码','总电流[A]','总电压[V]','总开关','充电状态','加热','SOC[%]','SOH[%]','单体均衡状态','单体电压1[mV]','单体电压2'
        ,'单体电压3','单体电压4','单体电压5','单体电压6','单体电压7','单体电压8','单体电压9','单体电压10','单体电压11','单体电压12','单体电压13','单体电压14','单体电压15','单体电压16'
        ,'单体电压17','单体温度1','单体温度2','单体温度3','单体温度4','其他温度1','其他温度2','其他温度3','其他温度4','其他温度5'],
        data=data_block
         )
    return df



if __name__ == "__main__":
    
    df_all = pd.DataFrame(
            columns=['编号','时间戳','GSM信号','故障等级','故障代码','总电流[A]','总电压[V]','总开关','充电状态','加热','SOC[%]','SOH[%]','单体均衡状态','单体电压1[mV]','单体电压2'
            ,'单体电压3','单体电压4','单体电压5','单体电压6','单体电压7','单体电压8','单体电压9','单体电压10','单体电压11','单体电压12','单体电压13','单体电压14','单体电压15','单体电压16'
            ,'单体电压17','单体温度1','单体温度2','单体温度3','单体温度4','其他温度1','其他温度2','其他温度3','其他温度4','其他温度5']
            )
    for line in download_json_data('url'):
        '''
        遍历生成器，将每次生成器迭代的行追加到df_all
        '''
        df_add = convert_to_dataframe(line)
        df_all = df_all.append(df_add,ignore_index=True)
    # df_all.loc[:,'时间戳'] = df_all.loc[:,'时间戳'].apply(lambda x:datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    print(df_all)

