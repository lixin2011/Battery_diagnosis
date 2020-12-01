import pandas as pd
import os
def get_path(): 
    '''
    返回电池数据文件具体路径
    '''
    # 创建工作目录，放置文件
    print('\n********************   程序的工作目录为D:\qixiang，请注意查看   ********************')
    try:
        os.mkdir(r'D:\qixiang')
        print('\n********************   目录D:\qixiang已创建   ********************')
    except FileExistsError:
        print('\n********************   目录D:\qixiang已存在   ********************')
    
    input('\n请在目录D:\qixiang放入单个电池数据文件(支持csv和xlsx文件，按回车继续)')
    # 选择文件
    os.chdir(r'D:\qixiang')  
    file_list = os.listdir(r'D:\qixiang')
    print('\n检测到的电池文件为：',file_list)
    file_path = 'D:\\qixiang\\' + file_list[0]
    return file_path

def get_data(path):
    '''
    输入文件路径，读取并返回所有电池数据
    '''
    file_type = path.split('.')[-1]
    print('\n********************   数据读取中，请稍候   ********************')
    if file_type == 'xlsx':
        data_all = pd.read_excel(path)
    elif file_type == 'csv':
        data_all = pd.read_csv(path,encoding='gbk')
    print('\n********************   数据读取完成   ********************')
    return data_all

def get_sn(data):
    '''
    输入数据，返回数据中存在的sn
    '''
    sn = data.iloc[:,0]
    sn_unique = list(pd.unique(sn))
    return sn_unique












