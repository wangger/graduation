import time
from datetime import datetime,timedelta
import numpy as np
import pandas as pd
from data_test5 import get_dataframe, read_data
from process_log import Valuefilling, log_Timesplit, log_Usersplit_feature, Userfeature_Process
from feature_extraction_1 import feature_concact, week_concact, get_listdata, w_list_txt


pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 500)

print("get log feature:")
#前期准备工作
#提取term_id，对应的开始时间和结束时间，duration
f_path = 'moc_term'
f_name = '000000_0'
delim = '\x01'
course_data = read_data(f_path,f_name,delim)
course_column = ['id','gmt_create','gmt_modified','course_id','start_time','duration','end_time','publish_status','small_photo','big_photo','course_load','first_publish_time','close_visable_status','web_visible','achievement_status','term_no','chargeable_cert','achievement_confirmed_time','time_to_freeze','mode','from_term_id','school_id','password','qualified_count','excellent_count','enroll_count','delta_start','delta_end','weight_total','weight_starting','weight_started','weight_finished','origin_copy_right_term_id','apply_mooc_status','from_term_mode','uniform_combo_score',  'mob_uniform_combo_score','copied','copy_time','price']
course_data = get_dataframe(course_data,course_column)
extract_column = ['id','course_id','start_time','end_time','duration']
course_data = course_data[extract_column]
test_course = course_data.ix[1]
term_id = test_course['id']
start_time = test_course['start_time']
end_time = test_course['end_time']
duration = test_course['duration']

starttime1 = datetime.now()
wda_name = 'wda.csv'
wda_data = pd.read_csv(wda_name)

wda_extract_column = ['logtime','url.1','uid','sid']
wda_data = wda_data[wda_extract_column]

wda_data['logtime'] = wda_data['logtime'].astype('str')

wda_data = wda_data.replace('-',np.nan)
wda_data = wda_data.replace(r'\N',np.nan)
wda_data = wda_data.replace('null',np.nan)
wda_data = wda_data.replace('NULL',np.nan)
wda_data = wda_data.replace('',np.nan)

wda_data = Valuefilling(wda_data,['logtime'],[[np.nan]],[['1653192600000']])

wda_data = wda_data.dropna(axis = 0)

endtime1 = datetime.now()
print("method datetime() : %f s" % (endtime1 - starttime1).seconds)

time_tag = 'logtime'
starttime1 = datetime.now()
timeseries = log_Timesplit(wda_data,start_time,end_time,duration,time_tag)

endtime1 = datetime.now()
print("method datetime() : %f s" % (endtime1 - starttime1).seconds)

#用户特征提取(仍然按周划分)
#timeseries中应该是没有什么nan了的！(有的话之前应该就被干掉了，除非还有缺失值的类型没覆盖到)
#删除重复列，确保user_tag不叫'user_id'(这里确实不叫)
starttime1 = datetime.now()
user_tag = 'uid'
user_label, user_feature = log_Usersplit_feature(timeseries,user_tag,term_id,time_tag)#term_id给test用
endtime1 = datetime.now()
print("method datetime() : %f s" % (endtime1 - starttime1).seconds)

#构成全量数据
#删除重复列，确保user_tag不叫'user_id'(这里确实不叫,,还是uid)
print('start to see user_feature')
user_feature = Userfeature_Process(user_feature, user_tag, term_id)

print('start to see user_label')
user_label = Userfeature_Process(user_label, user_tag, term_id)
#测试一下

#暂时就只能测试一下week连接会有什么效果
user_feature = week_concact(user_feature)
user_label = week_concact(user_label)
print("get log feature end")
print("***********************************************")
print("get ")
