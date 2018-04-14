#实验了读取文件（是文本文件，utf-8编码）的方法，找到了间隔符（\x01）
#try:
F_PATH = "user_tag_value"
F_NAME = "000000_0"
    #文件名用‘/’而不是'\\'没问题
'''
    f = open(F_PATH + '/'+ F_NAME, 'r',encoding = 'utf-8')#!!!!编码问题！（文件是utf-8的，不是ascii！）
    print(f)
    str = f.readline()
    print(str)
    str1 = '\x01'
    str = str.split(str1)#要把返回值赋予新的！！！不能直接调用函数不接收返回值！
    for string in str:
        print(string)
finally:
    if f:
        f.close()
'''
FILE_NAME = F_PATH + '/'+ F_NAME
with open(FILE_NAME, 'r',encoding = 'utf-8') as f:
    str = f.readline()
    print(str)
    str1 = '\x01'
    str = str.strip().split(str1)#要把返回值赋予新的！！！不能直接调用函数不接收返回值！(去掉了末尾换行！)
    print(str)
    for str_ele in str:
        print(str_ele)#!!!自动添加换行？？？！
#\x01是分隔符！！！(交互式环境中查看变量值而不是print才看得出不可打印字符！)
