from pandas import read_csv,read_excel
from os import mkdir,chdir,listdir
from tqdm import tqdm
def get_path(): 
    '''
    返回电池数据文件具体路径
    '''
    # 创建工作目录，放置文件
    print('\n********************   程序的工作目录为D:\qixiang，请注意查看   ********************')
    try:
        mkdir(r'D:\qixiang')
        print('\n********************   目录D:\qixiang已创建   ********************')
    except FileExistsError:
        print('\n********************   目录D:\qixiang已存在   ********************')
    
    # input('\n请在目录D:\qixiang放入单个电池数据文件(支持csv和xlsx文件，按回车继续)')
    # 选择文件
    chdir(r'D:\qixiang')  
    file_list = listdir(r'D:\qixiang')
    print('\n检测到的电池文件为：',file_list)
    file_path = 'D:\\qixiang\\' + file_list[0]
    return file_path

def get_data(path):
    '''
    输入文件路径，读取并返回所有电池数据
    '''
    file_type = path.split('.')[-1]
    print('\n********************   数据读取中，请稍候   ********************\n')
    with tqdm(total=100) as pbar:
        pbar.update(0)
        if file_type == 'xlsx':
            data = read_excel(path)
        elif file_type == 'csv':
            data = read_csv(path,encoding='gbk')
        pbar.update(100)
    print('\n********************   数据读取完成   ********************\n')
    columns_strip = data.columns.map(lambda x:x.strip())
    data.columns = columns_strip  
    # 清除掉数据表列索引中可能存在的空格 
    print(data.info())
    print(data.describe())
    print(data)
    return data














