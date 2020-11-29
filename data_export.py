import pandas as pd
import os

def export_temp(data):
    '''
    导出数据的温度项
    '''
    temp = data[['gmt_time','battemp']]
    return temp

def export_cur(data):
    '''
    导出数据的电流项
    '''
    cur = data[['gmt_time','batcurrent']] 
    return cur

def export_vol_total(data):
    '''
    导出数据的总电压项
    '''
    vol = data[['gmt_time','batvoltage']]
    return vol

def export_vol_mono(data):
    '''
    导出数据的单体电压项
    '''
    vol_mono = data[[18,8,9,10,11,12,13,14,15,16,17]]  
    return vol_mono

def export_cap_total(data):
    '''
    导出数据的总容量项
    '''
    cap = data[['gmt_time','batafcap']]           
    return cap

def export_cap_now(data):
    '''
    导出数据的当前容量项
    '''
    cap_now = data[['gmt_time','batrscap']]  
    return cap_now

def export_soc(data):
    '''
    导出数据的当前容量项
    '''
    soc = data[['gmt_time','batrsoc']]  
    return soc

def export_charge_count(data):
    '''
    导出数据的充电次数
    '''
    charge_count = data[['gmt_time','batchargecount']]
    return charge_count  
