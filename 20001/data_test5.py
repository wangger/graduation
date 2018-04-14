#超大文件的那个间隔符是“\t”
#想用pandas来进行创建dataframe!!!
#要进行函数封装了！
'''
    给函数写注释！
    list矩阵的转置函数
    创建出dataframe的函数
    #元素数据类型转换？！（默认dtype是object？type就是str）
    ？？读取文件的函数？？col_name？
    ？？datafram中元素的数据类型？numpy的数据类型？
    import numpy as np  ？？？外部文件调用函数时需要写这个吗？

    ！！！！将list都用narray处理！！！（效率高！！！）／series?
    numpy和pandas的关系？数据类型一致性？兼容性？
    python的object类型？还有一个正则表达式？

    dataframe行索引采用切片的方式！！！！
    ？？？pandas读取txt文件还是不会（？？？encoding?）
'''

'''
    是否也有list[]创建dict{}的方法呢(dict(zip()))
    ？？还有就是日志文件中的时间是按照时间先后顺序排列生成的吗
    ？？pandas读取和python io读取的效率问题
'''

import time
from datetime import datetime
import numpy as np
import pandas as pd

def get_dataframe(data,column_name):
    #data(2d),column_name(1d)为list,dtype为str, return dataframe(？？是一个引用吗？)
    try:
        #data = np.matrix(data)#这行可有可无
        #print("get matrix successfully")
        data = pd.DataFrame(data, columns = column_name)#这种方式不允许行列和数据不对应！！
    except:
        print("failed to get dataframe!")
        return
    else:
        #print(data.info())
        print("get dataframe successfully!")
        #输出一行
        #print(data.ix[0])
        #输出一列的长度
        #column = data.columns.values[0]
        #print(len(data[column]))
        #输出指定位置元素
        #print(data.ix[0:1,0:1])#前两行的第一列！！！（行包括1，列不包括1）很神奇的规定！！！！
        #print(data.ix[1,1])#这种就是[1,1]的位置
        return data

########################################
def list_2d_transpose_1(data):
    #data为list，return list
    #method1
    print("before transpose:" + str(len(data)))
    data = [[row[col] for row in data] for col in range(len(data[0]))]
    print("after transpose" + str(len(data)))
    return data

def list_2d_transpose_2(data):
    #data为list，return list
    #method2
    #!!!map和zip本身都不是返回list的！（zip换成list后，内部元素师tuple，还需要进一步转换）
    print("before transpose:" + str(len(data)))
    data = list(map(list,list(zip(*data))))
    print("after transpose" + str(len(data)))
    return data

def get_dataframe_trans(data,column_name):
    #data为list，转置的，每行都是一列的数据！
    try:
        data = dict(list(zip(column_name,data)))
        #用字典创建dataframe
        data = pd.DataFrame(data)
    except:
        print("failed to get dataframe!")
        return
    else:
        #print(data.info())
        print("get dataframe successfully!")
        #输出一行
        print(data.ix[0])
        #输出一列的长度
        column = data.columns.values[0]
        print(len(data[column]))
        #输出指定位置元素
        print(data.ix[0:1,0:1])#前两行的第一列！！！（行包括1，列不包括1）很神奇的规定！！！！
        print(data.ix[1,1])#这种就是[1,1]的位置
        return data
##############################################

def read_data(f_path, f_name,delimiter):
#all the arguments are str, the type of return value is list_2d(every element is a row record)
    #开始读取大文件了
    file_name = f_path + '/' + f_name
    info = []
    with open(file_name, 'r', encoding = 'utf-8') as f:
        for line in f.readlines():#list,line为每条记录
            #temp =dict(zip(col_name,line.strip().split('\t')))
            #print(temp)
            temp = line.strip().split(delimiter)#去尾
            info.append(temp)
            #print("the total number of records: %d" % len(info))
            #print(len(col_name))
            #print(len(info[0]))
            #total_num = 0
            '''
            for i in range(len(col_name)):
                total_num = total_num + 1
                print(col_name[i] in info[0])
                print(str(i) + ", "+ col_name[i] +", "+ info[0][col_name[i]])
            print(total_num)
            '''
    return info