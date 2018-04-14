#开始正式对数据进行探索，用的多的尝试进行函数封装
'''
experiments
1.判断是否按照时间排序？或者说直接排序，看看花的时间多不多
2.时间排序好的基础上看看能不能把数据进行按周切分？
3.看看数据能不能按照用户group by或者说得到一些统计量
4.争取能封装出一套数据处理的函数
5.uid那个关联是否可用？
'''
'''
answer
1.wda表很快，应该是按照时间排序的

'''
import time
from datetime import datetime
import numpy as np
import pandas as pd
from data_test5 import get_dataframe, read_data


data = pd.read_csv('wda.csv',encoding = 'utf-8')
print(data.ix[0])

'''
print("test1 start")
start_time1 = datetime.now()
data = pd.read_csv('wda.csv',encoding = 'utf-8')
data = data.sort_values(by = "logtime", ascending = True)
for i in range(10):
    print(data.ix[i])
end_time1 = datetime.now()
print("the time to sort is %f s." % (end_time1 - start_time1).seconds)
print("********************************")
'''
