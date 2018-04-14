#超大文件的那个间隔符是“\t”
'''
    测试读取100m文件的速度
    看看python的时间函数的用法
    time.clock() 单位是秒
    time.time() 单位也是秒
    datetime.seconds这个方法貌似四舍五入了？
'''
#method time.time() : 3.895969 s

#尝试转化下时间戳！
'''
    时间数据取前十位！后面是小数点了！
'''

import time
from datetime import datetime
starttime1 = datetime.now()
starttime2 = time.time()
starttime3 = time.clock()

#开始读取大文件了
F_PATH = 'wda_mooc'
F_NAME = 'wda_mooc_10001.txt'
file_name = F_PATH + '/' + F_NAME
info = []#存储信息

with open(file_name, 'r', encoding = 'utf-8') as f:
    for line in f.readlines():#list,line为每条记录
        info.append(line.strip().split('\t'))
print("the total number of records: %d" % len(info))
print(info[0])

#时间戳转化为datetime
timestamp = int(info[-1][0])/1000
print(timestamp)
print(datetime.fromtimestamp(timestamp))

endtime1 = datetime.now()
endtime2 = time.time()
endtime3 = time.clock()
print("method datetime() : %f s" % (endtime1 - starttime1).seconds)#??类型对吗
print("method time.time() : %f s" % (endtime2 - starttime2))
print("method time.clock() : %f s" % (endtime3 - starttime3))
