import json
import os
import requests
import time
import csv
import pandas as pd

os.chdir(r'D:\temp')

def read_data(local_csv_name):
    '''
    在本地生成符合上传格式的json文件,命名为'bat.json'
    '''
    df = pd.read_csv(local_csv_name,encoding='gbk')
    print(df)
    file_in = csv.reader(open(local_csv_name,'r'))
    file_out_name = 'bat.json'
    file_out = open(file_out_name,'a')
    count = 0
    for line in file_in:
        if count != 0 and line:
            print('\n本地数据\n')
            print(line)
            info_dict = dict.fromkeys(('devcode','obdTime','receiveTime','dataType','subType','isBlindData','familyId'),
                                        0)
            status_dict = dict.fromkeys(('rssi','errorLevel','errorCode','current','voltageInner','voltageOutter','switchState',
                                        'soc','soh','cellVolBalance','cellVoltageCount','cellTempCount','otherTempCount',
                                        'cellVoltageList','cellTempList','otherTempList','totalOutputState','heatState',
                                        'chargeState','blueOpenState','blueConnectState','lockedState','rentalState','cellVoltageDiff',
                                        ),
                                        0)
            info_dict['receiveTime'] = int(time.time()*1000)              
            info_dict['dataType'] = 12
            info_dict['devcode'] = line[0]
            status_dict['cellTempCount'] = 1
            status_dict['cellTempList'] = [float(line[1])]
            status_dict['cellVoltageCount'] = 1
            status_dict['cellVoltageList'] = [float(line[3])/1000]
            status_dict['current'] = float(line[2])/1000
            status_dict['soc'] = line[4]
            # status_dict['batrscap'] = line[5]
            # status_dict['batafcap'] = line[6]
            # status_dict['chargecount'] = line[7]
            status_dict['cellVoltageCount'] = 10
            status_dict['cellVoltageList'] = [float(line[i])/1000 for i in range(8,18)]
            status_dict['otherTempList'] = [0]
            time_array = time.strptime(line[18],'%Y/%m/%d %H:%M:%S')
            time_stamp = time.mktime(time_array)
            info_dict['obdTime'] = int(time_stamp*1000)
            if line[19] == '充电':
                status_dict['chargeState'] = 2
            elif line[19] == '放电':
                status_dict['chargeState'] = 3
            bat_dict = {'info':info_dict,'ffBatteryStatus':status_dict}
            line_json = json.dumps(bat_dict)
            print(line_json)
            file_out.write(line_json)
            file_out.write('\n')
        count += 1 
    file_out.close()
    return file_out_name

def upload_data(local_json_name):
    file = open(local_json_name,'r')
    for line in file:
        print('-------- uploading -------')
        print(line)
        headers = {'Content-Type': 'application/json'}
        file_upload = requests.post('url_for_save',data=line,headers=headers).text
        print(file_upload)



file_out_name = read_data('BAA3219031600099.csv')
# upload_data(file_out_name)






