#超大文件的那个间隔符是“\t”
#想用pandas来进行创建dataframe
'''
    ？？是否也有list[]创建dict{}的方法呢
    编程dict也不太好！本质是希望通过a[num][‘col_num’]来索引吧
    (只是一种尝试，我认为肯定还是pandas那种操作和索引比较方便)
    py没有++?
    dic顺序会变
    为啥列数一致性检验会出问题？？？（dic的len）
    len有玄机？？？
'''

'''
    ？？还有就是日志文件中的时间是按照时间先后顺序排列生成的吗
    ？？pandas读取和python io读取的效率问题
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
col_name = ['logtime','login_type','filter','version','session_seq','hostname','character_set','screen_resolution','screen_color','language','flash_version','refer','url','os','browser','browser_version','uid','sid','first_session','last_session','current_session','ip','region','event_category','event_operation','event_label','daily_newuser','hourly_newuser','search_keyword','search_engine','referral','source','medium','utm_source','utm_medium','utm_campaign','custom_data','dt','type','url','refer']
with open(file_name, 'r', encoding = 'utf-8') as f:
    for line in f.readlines():#list,line为每条记录
        temp =dict(zip(col_name,line.strip().split('\t')))
        #print(temp)
        info.append(temp)
print("the total number of records: %d" % len(info))
print(len(col_name))
print(len(info[0]))
total_num = 0
for i in range(len(col_name)):
    total_num = total_num + 1
    print(col_name[i] in info[0])
    print(str(i) + ", "+ col_name[i] +", "+ info[0][col_name[i]])
print(total_num)
#时间戳转化为datetime
timestamp = int(info[-1]['logtime'])/1000
print(timestamp)
print(datetime.fromtimestamp(timestamp))

endtime1 = datetime.now()
endtime2 = time.time()
endtime3 = time.clock()
print("method datetime() : %f s" % (endtime1 - starttime1).seconds)#??类型对吗
print("method time.time() : %f s" % (endtime2 - starttime2))
print("method time.clock() : %f s" % (endtime3 - starttime3))
