import time
from datetime import datetime,timedelta
import numpy as np
import pandas as pd
from data_test5 import get_dataframe, read_data
from process_log import Valuefilling, log_Timesplit, log_Usersplit_feature, Userfeature_Process
from feature_extraction_1 import feature_concact, week_concact, get_listdata, w_list_txt


pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 500)
'''
dt = datetime(2022,5,22,12,10)
dt = dt.timestamp()
print(dt)
#1653192600000
'''

print("test1 start:")
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
#print(course_data.describe)
#print(course_data.dtypes)
#测试可知有5个学期，每个学期持续的时间并不一样，然后id和course_id在这个表中没有乱，并且所有数据都是object(时间和duration都是str)
#一门课有不同的学期，针对一个学期的数据进行单独预测
#尝试采用第2学期的数据即可
test_course = course_data.ix[1]
#print(test_course)
term_id = test_course['id']
start_time = test_course['start_time']
end_time = test_course['end_time']
duration = test_course['duration']

#准备工作结束，正式进行特征提取
#先打开并合并出要提取特征的wda(包含的是所有学期的数据,但此处也不用提取对应学期的，因为timesplit本身就能截取出这个学期的数据，但是然后最后的user merge那里需要term_id)
starttime1 = datetime.now()
wda_name = 'wda.csv'
wda_data = pd.read_csv(wda_name, nrows = 30000)
#print(len(wda_data))
#print(wda_data.columns)
#print(wda_data.head(10))
wda_extract_column = ['logtime','url.1','uid','sid']
wda_data = wda_data[wda_extract_column]
#print(len(wda_data))
#print(wda_data.ix[0])
#print(wda_data.dtypes)
#logtime是int64
wda_data['logtime'] = wda_data['logtime'].astype('str')
#对数据进行缺失值的填充(时间数据)
#用什么时间填充呢
#'1653192600000'
#缺失值是np.nan?
#缺失值（防止logtime中有缺失值）
wda_data = wda_data.replace('-',np.nan)
wda_data = wda_data.replace(r'\N',np.nan)
wda_data = wda_data.replace('null',np.nan)
wda_data = wda_data.replace('NULL',np.nan)
wda_data = wda_data.replace('',np.nan)
#print("before processing missing value")
#print (wda_data.isnull().any())
#print(wda_data[wda_data.isnull().values == True])
#print(wda_data.dtypes)
#print(wda_data.ix[0,'url.1'])
wda_data = Valuefilling(wda_data,['logtime'],[[np.nan]],[['1653192600000']])
#删除有缺失值的行(不知道url/uid/sid的行，所以之后wda的赋值那块就不担心有缺失值了,不需要在函数内考虑此类情况了)
wda_data = wda_data.dropna(axis = 0)
#print(len(wda_data))
#print("after processing missing value")
#print (wda_data.isnull().any())
#print(wda_data[wda_data.isnull().values == True])
#print(wda_data.dtypes)
#print(wda_data.head(100))
#print(wda_data.ix[0,'url.1'])
#时间数据在函数(timesplit)内有进行过排序
#都是str
endtime1 = datetime.now()
print("method datetime() : %f s" % (endtime1 - starttime1).seconds)

time_tag = 'logtime'
starttime1 = datetime.now()
#时间切割(自动切出了对应学期的)
timeseries = log_Timesplit(wda_data,start_time,end_time,duration,time_tag)
#看看情况
#区别在于timepiece中时间没有被drop而是作为一个列属性保留了下来，10位int
#timeseries中的dataframe按照时间顺序排列，索引自增
endtime1 = datetime.now()
print("method datetime() : %f s" % (endtime1 - starttime1).seconds)
starttime1 = datetime.now()

#sum_record = 0
'''
for timepiece in timeseries:
    #print(timepiece.isnull().any())
    #print(timepiece[timepiece.isnull().values == True])
    #print(timepiece.info())
    #print(timepiece.dtypes)
    #print(timepiece.describe())
    #print(timepiece.index)
    #print(timepiece.columns)
    #print(timepiece.ix[0])
    #print(timepiece.ix[1])
    sum_record = sum_record + len(timepiece)
'''
#print(sum_record)
endtime1 = datetime.now()
print("method datetime() : %f s" % (endtime1 - starttime1).seconds)

print(timeseries[0].dtypes)


#用户特征提取(仍然按周划分)
#timeseries中应该是没有什么nan了的！(有的话之前应该就被干掉了，除非还有缺失值的类型没覆盖到)
#删除重复列，确保user_tag不叫'user_id'(这里确实不叫)
starttime1 = datetime.now()
user_tag = 'uid'
user_label, user_feature = log_Usersplit_feature(timeseries,user_tag,term_id,time_tag)#term_id给test用
endtime1 = datetime.now()
print("method datetime() : %f s" % (endtime1 - starttime1).seconds)

#看看情况
'''
for userpiece in user_feature:#每周的按用户分类后的情况
   #print(userpiece.ix[0])
    print(userpiece.index)
    print(userpiece.info())
    print(userpiece.dtypes)
    print(userpiece.describe())
    print('lenth is :' + str(len(userpiece)))
    print(type(userpiece))

print('start to see labels:')
for userpiece in user_label:#每周的第一个用户
    #print(userpiece.ix[0])
    print(userpiece.info())
    print(userpiece.dtypes)
    print(userpiece.describe())
    print('lenth is :' + str(len(userpiece)))
    print(type(userpiece))

print(duration)
'''
#构成全量数据
#删除重复列，确保user_tag不叫'user_id'(这里确实不叫,,还是uid)
print('start to see user_feature')
user_feature = Userfeature_Process(user_feature, user_tag, term_id)
'''
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
'''
print('start to see user_label')
user_label = Userfeature_Process(user_label, user_tag, term_id)
#测试一下
'''
print(type(user_label[0]))
print(user_label[0].index)
print (user_label[0].isnull().any())
print(user_label[0][user_label[0].isnull().values == True])

for userpiece in user_label:#每周的第一个用户
    print(userpiece.ix[0])
    print(userpiece.info())
    print(userpiece.dtypes)
    print(userpiece.describe())
    print('lenth is :' + str(len(userpiece)))
'''

#暂时就只能测试一下week连接会有什么效果
user_feature = week_concact(user_feature)
'''
print(user_feature.ix[0])
print(duration)
'''
user_label = week_concact(user_label)
'''
print(user_label.ix[0])
print(duration)
'''
print("test1 end")
