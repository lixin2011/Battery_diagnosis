import pandas as pd
import os

def get_sampling_rate(data):
    '''
    输入数据，获取其时间间隔的均值
    '''
    time = data.index
    diff = time.diff(periods=1).apply(lambda x:x.seconds)
    diff_mean =diff.mean()
    return diff_mean

