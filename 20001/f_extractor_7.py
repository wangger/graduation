import time
from datetime import datetime,timedelta
import numpy as np
import pandas as pd
from data_test5 import get_dataframe, read_data
from feature_extraction_1 import Valuefilling, Timesplit, Usersplit_times,Usersplit_sum, Userfeature_Process, feature_concact, week_concact, get_listdata, w_list_txt

#该时间段内用户发布评论的总数


pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 500)
'''
dt = datetime(2022,5,22,12,10)
dt = dt.timestamp()
print(dt)
#1653192600000
'''

print("test1 start:")
#尝试生成log特征
#前期准备工作
#提取term_id，对应的开始时间和结束时间，duration
f_path = 'moc_term'
f_name = '000000_0'
delim = '\x01'
course_data = read_data(f_path,f_name,delim)
course_column = ['id','gmt_create','gmt_modified','course_id','start_time','duration','end_time','publish_status','small_photo','big_photo','course_load','first_publish_time','close_visable_status','web_visible','achievement_status','term_no','chargeable_cert','achievement_confirmed_time','time_to_freeze','mode','from_term_id','school_id','password','qualified_count','excellent_count','enroll_count','delta_start','delta_end','weight_total','weight_starting','weight_started','weight_finished','origin_copy_right_term_id','apply_mooc_status','from_term_mode','uniform_combo_score',  'mob_uniform_combo_score','copied','copy_time','price']
course_data = get_dataframe(course_data,course_column)
extract_column = ['id','course_id','start_time','end_time','duration']#id即term_id
course_data = course_data[extract_column]
#print(course_data)
#print(course_data.dtypes)
#测试可知有5个学期，每个学期持续的时间并不一样，然后id和course_id在这个表中没有乱，并且所有数据都是object(时间和duration都是str)
#一门课有不同的学期，针对一个学期的数据进行单独预测
#尝试采用第二学期的数据即可
test_course = course_data.ix[1]
#print(test_course)
#都是str
term_id = test_course['id']
start_time = test_course['start_time']
end_time = test_course['end_time']
duration = test_course['duration']

#准备工作结束，正式进行特征提取
#先打开并合并出要提取特征的dataframe(包含的是所有学期的数据)

#comment文件
comment_path = 'moc_comment'
comment_name = '000000_0'
p_delim = '\x01'
comment_data = read_data(comment_path, comment_name, p_delim)
comment_column = ['id', 'gmt_create', 'gmt_modified', 'commentor_id', 'anonymous', 'post_id', 'reply_id', 'count_vote', 'comment_time', 'deleted', 'tag_agree', 'tag_top', 'tag_top_time', 'active_flag', 'forum_id', 'term_id']
comment_data = get_dataframe(comment_data, comment_column)
comment_extract_column = ['comment_time','commentor_id']
comment_data = comment_data[comment_extract_column]
#对数据进行缺失值的填充(时间数据)
#用什么时间填充呢？
#'1653192600000'
#缺失值是np.nan吗
#缺失值（防止post_time中有缺失值）
comment_data = comment_data.replace('-',np.nan)
comment_data = comment_data.replace(r'\N',np.nan)
comment_data = comment_data.replace('null',np.nan)
comment_data = comment_data.replace('NULL',np.nan)
comment_data = comment_data.replace('',np.nan)
comment_data = Valuefilling(comment_data,['comment_time'],[[np.nan]],[['1653192600000']])
#删除有缺失值的行(不知道poster_id/content的行)
comment_data = comment_data.dropna(axis = 0)

print (comment_data.isnull().any())
print(comment_data[comment_data.isnull().values == True])
print(comment_data.ix[0])

time_tag = 'comment_time'
#时间数据在函数内有进行过排序???
#时间切割(自动切出了对应学期的)
timeseries = Timesplit(comment_data,start_time,end_time,duration,time_tag)
#看看情况
for timepiece in timeseries:
    print(timepiece.isnull().any())
    print(timepiece[timepiece.isnull().values == True])
    print(timepiece.info())
    print(timepiece.dtypes)
    print(timepiece.describe())
    print(timepiece.ix[0])
    print(timepiece.ix[1])
    print(timepiece.ix[-1])

#用户切割(size())
#timeseries中应该是没有什么nan了的！
user_tag = 'commentor_id'
user_feature = Usersplit_times(timeseries,user_tag)

#看看情况
for userpiece in user_feature:#每周的第一个用户
    print(userpiece.ix[0])
    print(userpiece.info())
    print(userpiece.dtypes)
    print(userpiece.describe())
    print('lenth is :' + str(len(userpiece)))
    print(type(userpiece))

#构成全量数据
#删除重复列，确保user_tag不叫'user_id'(这里确实不叫)
user_feature = Userfeature_Process(user_feature, user_tag, term_id)
#测试一下
print(type(user_feature[0]))
print(user_feature[0].index)
print (user_feature[0].isnull().any())
print(user_feature[0][user_feature[0].isnull().values == True])

for userpiece in user_feature:#每周的第一个用户
    print(userpiece.ix[0])
    print(userpiece.info())
    print(userpiece.dtypes)
    print(userpiece.describe())
    print('lenth is :' + str(len(userpiece)))

#暂时就只能测试一下week连接会有什么效果
user_feature = week_concact(user_feature)
print(user_feature.ix[0])
print(duration)

print("test1 end")

