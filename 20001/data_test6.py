#开始正式对数据进行探索，用的多的尝试进行函数封装
'''
experiments
1.moc_reply和moc_comment是否索引与内容不对应 
2.dataframe的构造函数是否好用，dataframe中所有数据的dtype
3.尝试一些dataframe的查看属性的函数
#对wda进行一波探索
4.wda中数据的大致情况，单行数据类型的变换？时间数据是否是按照降序排列？
dataframe中的列是否也是dataframe？
dataframe可否比较相等？
13位的时间戳是否溢出？
？？如何获取每一列的describe？？？（交互式环境实验？？ sid,uid这种）
???是否把dataframe输出一下呢？？？转化貌似很慢

5.比较探索一下是否是按照降序排列的（wda本身）
6.看一下wda表中的人(确认有浏览记录的？)是否出现在user中(注册用户) #也许可以通过观察完成test8，完不成再单独在6基础上加
7.???封装读取多个文件的函数？（仅限本文件夹下数据的使用）
8.选课时间和最后一次登陆时间是不是在wda表中出现了呢？？？
9.dataframe的数据库拼接操作！是concat不是join！（join将行索引合并）应该是merge！
'''

'''
answer
1.lack of term_id! Is term id a defalut value? 感觉其实差的是content？？？term_id没毛病？？
2.it worked! it is able to catch errors successfully!
  all the data is str！
3.describe() is very useful! It offers a lot of statistics value??
4.completing data transforming successfully! df.sort_values( by = []) 
ascending : bool or list of bool, default True
Sort ascending vs. descending. Specify list for multiple sort orders. If this is a list of bools, must match the length of the by.
   
是series！
Series.equals(other)！！！可以按顺序比较是否相等的！
no overflow
？？
？？

'''

import time
from datetime import datetime
import numpy as np
import pandas as pd
from data_test5 import get_dataframe, read_data
'''
print('test1 start')
f_path = 'moc_reply'
f_name = '000000_0'
info = read_data(f_path,f_name,'\x01')
print(info[0])
print("the number of elements in each record : %d " % len(info[0]))
col_name = ['id', 'gmt_create', 'gmt_modified', 'replyer_id', 'anonymous', 'post_id', 'content', 'count_vote', 'count_comment', 'reply_time', 'deleted', 'tag_agree', 'tag_top', 'tag_top_time', 'active_flag', 'forum_id', 'term_id'
]
print("the number of elements in col_name : %d" % len(col_name))

f_path = 'moc_comment'
info = read_data(f_path,f_name,'\x01')
print(info[0])
print("the number of elements in each record : %d " % len(info[0]))
col_name = ['id', 'gmt_create', 'gmt_modified', 'commentor_id', 'anonymous', 'post_id', 'reply_id', 'content', 'count_vote', 'comment_tiem', 'deleted', 'tag_agree', 'tag_top', 'tag_top_time', 'active_flag', 'forum_id', 'term_id']
print("the number of elements in col_name : %d" % len(col_name))

print('test1 end')

print('*************************************')
print('test2 start')
#删去对不上的term_id
col_name = ['id', 'gmt_create', 'gmt_modified', 'commentor_id', 'anonymous', 'post_id', 'reply_id', 'content', 'count_vote', 'comment_tiem', 'deleted', 'tag_agree', 'tag_top', 'tag_top_time', 'active_flag', 'forum_id']
data = get_dataframe(info,col_name)
#输出一行
print(data.ix[0])
#输出一列的长度
column = data.columns.values[0]
print(len(data[column]))
#输出指定位置元素
print(data.ix[0:1,0:1])#前两行的第一列！！！（行包括1，列不包括1）很神奇的规定！！！！貌似又不对？
print(data.ix[1,1])#这种就是[1,1]的位置
print('test2 end')
print('*************************************')
'''
'''
print('test3 start')
print(data.dtypes)
print(data.info())
print(data.describe())
print('test3 end')
print('*************************************')
'''
'''
print('test4 start')

wda_path = 'wda_mooc'
wda_name = 'wda_mooc_10001.txt'
wda_delim = '\t'
wda_data = read_data(wda_path,wda_name,wda_delim)
wda_col = ['logtime','login_type','filter','version','session_seq','hostname','character_set','screen_resolution','screen_color','language','flash_version','refer','url','os','browser','browser_version','uid','sid','first_session','last_session','current_session','ip','region','event_category','event_operation','event_label','daily_newuser','hourly_newuser','search_keyword','search_engine','referral','source','medium','utm_source','utm_medium','utm_campaign','custom_data','dt','type','url','refer']
wda_data = get_dataframe(wda_data,wda_col)

print("before transform type:")
print(wda_data.describe())
print(wda_data.dtypes)
print(wda_data.info())

print("after transform type:")
wda_data['logtime'] = wda_data['logtime'].astype(int)
print(wda_data.describe())
print(wda_data.dtypes)
print(wda_data.info())

print(wda_data.ix[0])
print('test4 end')
print('*************************************')
print(type(wda_data['logtime'])) #series？
print('test5 start')
origin_time = wda_data['logtime']
sort_time = origin_time.sort_values(ascending = True)
print(" is equal?" + str(origin_time.equals(sort_time)))
print('test5 end')
print('*************************************')
print('test6 start')
'''
user_path = 'user_tag_value'
user_infos = []
for val in range(37):
    if val < 10:
        user_name = '00000'+str(val)+'_0'
    else:
        user_name = '0000'+str(val)+'_0'
    user_filename = user_path + '/' + user_name
    with open(user_filename, 'r', encoding = 'utf-8') as f:
        temp_infos = f.readlines()
        for temp_info in temp_infos:
            user_infos.append(temp_info.strip().split('\x01'))
print("用户记录总数" + str(len(user_infos)))
#用户信息也要转化为dataframe
user_col = ['user_id','nickname','birthday','sex','region','last_time_in_mooc','course_id','term_id','choose_time']
user_infos = get_dataframe(user_infos,user_col)
print(user_infos.info())
#print(user_infos.ix[0])

#处理缺失值(\N!!!)
user_infos['last_time_in_mooc'] = user_infos['last_time_in_mooc'].replace(r'\N','2019-01-01')
user_infos['choose_time'] = user_infos['choose_time'].replace(r'\N','2019-01-01')
user_infos['last_time_in_mooc'] = pd.to_datetime(user_infos['last_time_in_mooc'])
user_infos['choose_time'] = pd.to_datetime(user_infos['choose_time'])
user_infos = user_infos.sort_values( by = "choose_time", ascending = True)
user_infos = user_infos.reset_index(drop = True)
print(user_infos.ix[0:10,'choose_time'])
#print(user_infos['choose_time'].head(5))
#for i in range(10):
#    print(user_infos.ix[i,'choose_time'])
'''
print("开始查看是否能对上")
test_user = wda_data.ix[0,'uid']
#应该都是字符串吧？没修改过这个类型
temp = user_infos[user_infos.user_id == test_user]
if(temp.empty):
      print("wda_uid not in user_id")
else:
      print("wda_uid exists in user_id, user_tag_record:")
      print(temp)
      temp2 = wda_data[wda_data.uid == test_user]
      print("correspeonding wda_record:")
      print(temp2)
print('test6 end')
print('*************************************')
'''

