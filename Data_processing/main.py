# -*- coding: utf-8 -*-

import data_input
import data_select
import data_export
import data_clean
import data_check

class battery():
    data = '数据为空'
    path = '路径为空'
    sn = '未筛选编号项'
    time_start = '未筛选开始时间项'
    time_end = '未筛选结束时间项'
    state = '未筛选状态项'
    # 筛选的单项数据
    temp = '未导出温度项'
    cur = '未导出电流项'
    vol_total = '未导出总电压项'
    vol_mono = '未导出单体电压项'
    cap_total = '未导出总容量项'
    cap_now = '未导出当前容量项'
    soc = '未导出soc项'
    charge_count = '未导出充电次数项'
    sampling_rate = '未检查采样频率'
    data_effect = '未进行数据有效性检查'
    def __init__(self):
        self.path = data_input.get_path()
        self.data = data_input.get_data(self.path)
    def select_with_sn(self):
        sn_list = data_select.get_sn(self.data)
        print('\n已上传的电池编号如下：',sn_list)
        sn_num_list = input("\n输入想要查询的电池编号（使用列表序号，序号从0开始）（用空格隔开）（可为空，查询所有数据）：")
        if sn_num_list != '':
            sn_num_list = sn_num_list.split(' ') 
            sn_num_list = [int(sn_num_list[i]) for i in range(len(sn_num_list))]
            sn_list_selected = [sn_list[i] for i in sn_num_list]
        else:
            sn_list_selected = ''
        self.sn = sn_list_selected
        self.data = data_select.select_sn(self.data,self.sn)
    def select_with_state(self):
        state_list = data_select.get_state(self.data)
        print('\n已上传的电池状态如下：',state_list)
        state_num_list = input("\n输入想要查询的电池状态（使用列表序号，序号从0开始）（用空格隔开）（可为空，查询所有数据）：")
        if state_num_list != '':
            state_num_list = state_num_list.split(' ') 
            state_num_list = [int(state_num_list[i]) for i in range(len(state_num_list))]
            state_list_selected = [state_list[i] for i in state_num_list]
        else:
            state_list_selected = ''
        self.state = state_list_selected
        self.data = data_select.select_state(self.data,self.state)
    def select_with_time(self):
        self.time_start = input('\n输入查询起始时间（任选年或月或日以及其组合，使用空格隔开）（可为空，查询之前的数据，包括当前时间点）：')
        self.time_end = input('\n输入查询终止时间（任选年或月或日以及其组合，使用空格隔开）（可为空，查询以后的数据，包括当前时间点）：')
        self.data = data_select.select_time(self.data,self.time_start,self.time_end)
    def export_data(self):
        self.temp = data_export.export_temp(self.data)
        self.cur = data_export.export_cur(self.data)
        self.vol_total = data_export.export_vol_total(self.data)
        self.vol_mono = data_export.export_vol_mono(self.data)
        self.cap_total = data_export.export_cap_total(self.data)
        self.cap_now = data_export.export_cap_now(self.data)
        self.soc = data_export.export_soc(self.data)
        self.charge_count = data_export.export_charge_count(self.data)
    def clean_data(self):
        self.data = data_clean.delete_na(self.data)
        self.data = data_clean.delete_value_0(self.data,'batvoltage')
        self.data = data_clean.delete_difference_irrational(self.data,'batchargecount')
        #只能解决跳变一个值的数据
        self.data = data_clean.delete_difference_irrational(self.data,'gmt_time')
        #可以删除多个重采样的值，只保存一个
        self.data = data_clean.delete_vol_wave(self.data)
    def check_quality(self):
        self.sampling_rate = data_check.get_sampling_rate(self.data)
        # self.data_effect = data_quality.get_data_effect(self.data)



    

if __name__ == "__main__":
    bat1 = battery()
    bat1.select_with_sn()
    bat1.select_with_state()
    bat1.select_with_time()















