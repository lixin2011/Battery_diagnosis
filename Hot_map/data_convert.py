import json,csv
import pandas as pd
import os

from pandas.io.parsers import count_empty_vals

os.chdir(r'C:\Data')
file = open(r'miles.json','w')
with open(r'C:\Data\count.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        if reader.line_num == 1:
            continue
        lng = line[1]
        lat = line[0]
        count = line[2]
        print(lng)
        print(lat)
        str_temp = '{"lng":'+str(lng)+',"lat":'+str(lat)+',"count":'+str(count)+'},\n'
        file.write(str_temp)