from datetime import datetime
import pandas as pd
import json
import os
import requests
import numpy as np
os.chdir(r'D:/temp')
def download_json_data(url):
    '''
    返回json数据的生成器，一次一行
    '''
    r = requests.get(url,stream=True)
    for line in r.iter_lines():
        if line:
            print('\n------------  downloading  ------------\n')
            yield json.loads(line)
        

if __name__ == "__main__":
    dataType = 12
    for sn in range(400,1000):
        file = open('dataType='+str(dataType)+'&sn=PK50001A100000'+str(sn)+'.json','a')
        for line in download_json_data('url?dataType='+str(dataType)+'&sn=PK50001A100000'+str(sn)+'&limit=1000000'):
            '''
            遍历生成器
            '''
            if line:
                print(line)
                line_json = json.dumps(line)
                file.write(line_json)
                file.write('\n')
        file.close()



