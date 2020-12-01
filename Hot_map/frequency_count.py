import os
import pandas as pd
'''
# 将所有的经纬度加载到一个文件
sn_list = os.listdir(r'C:\Data\map')
df_loc = pd.DataFrame(columns=['lng','lat'])
for sn in sn_list:
    os.chdir(r'C:\Data\map\\'+sn)
    day_list = os.listdir(r'C:\Data\map\\'+str(sn))
    for day_len in range(len(day_list)):
        df = pd.read_csv(day_list[day_len],encoding='gbk')
        df_temp = pd.DataFrame(columns=['lng','lat'])
        df_temp.lng = df.loc[:,'经度']
        df_temp.lat = df.loc[:,'纬度']
        df_loc = pd.concat([df_loc,df_temp])
        print(df_loc)
df_loc.to_csv(r'C:\Data\map\data_loc.csv')
'''
# 进行计数
df = pd.read_csv(r'C:\Data\map\data_loc.csv',encoding='gbk')
df.loc[:,'lng'] = df.loc[:,'lng'].round(2)
df.loc[:,'lat'] = df.loc[:,'lat'].round(2)

dup = df.loc[:,'lng'].groupby(df.loc[:,'lat']).value_counts()
dup.to_csv(r'C:\Data\count.csv',encoding='gbk')
print(dup)

