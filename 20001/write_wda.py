#开始正式对数据进行探索，用的多的尝试进行函数封装
'''
experiments
1.dataframe的数据库拼接操作！是concat不是join！(join将行索引合并)应该是merge！
(user_tag_value和moc_post)
'''

'''
answer


'''
import time
from datetime import datetime
import numpy as np
import pandas as pd
from data_test5 import get_dataframe, read_data


pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 500)

'''
print('test1 start')
f_path = 'moc_post'
f_name = '000000_0'
info_post = read_data(f_path,f_name,'\x01')
print('post is ok')

f2_path = 'user_tag_value'
info_user = []
for x in range(37):
    if x < 10:
        f2_name = '00000'+ str(x) + '_0'
    else:
        f2_name = '0000' + str(x) + '_0'
    user_filename = f2_path + '/' +f2_name
    with open(user_filename, 'r', encoding = 'utf-8') as f:
        temp_infos = f.readlines()
        for temp_info in temp_infos:
            info_user.append(temp_info.strip().split('\x01'))
print('user is ok')

post_colname = ['id','gmt_create','gmt_modified','type','lesson_unit_id','forum_id','root_forum_id','term_id','poster_id','post_time','title','last_replyer','last_reply_time','anonymous','tag_agree','tag_top','tag_top_time','tag_solve','tag_lector','count_browse','count_reply','count_vote','deleted','active_flag','lock_flag']

user_colname = ['user_id','nickname','birthday','sex','region','last_time_in_mooc','course_id','term_id','choose_time']

info_post = get_dataframe(info_post, post_colname)
info_user = get_dataframe(info_user, user_colname)


print(len(info_user))

test_result_inner = pd.merge(info_user,info_post,left_on = ['user_id','term_id'],right_on = ['poster_id','term_id'], how = 'inner')
print("inner lenth :" + str(len(test_result_inner)))
test_result_outer = pd.merge(info_user,info_post,left_on = ['user_id','term_id'],right_on = ['poster_id','term_id'], how = 'outer')
print("outer lenth :" + str(len(test_result_outer)))
test_result_left = pd.merge(info_user,info_post,left_on = ['user_id','term_id'],right_on = ['poster_id','term_id'], how = 'left')
print("left lenth :" + str(len(test_result_left)))
print('test_inner')
print(test_result_inner.head(20))

test_miss = test_result_outer[test_result_outer['user_id'].isnull() == True]
print('miss_lenth' + str(test_miss))
print('test1 end')
print('*************************************')
print('test2 start')

is_exist = info_user[info_user['user_id'] == '2163902']
print(is_exist['term_id'])
#is_exist2 = info_user[info_user['user_id'] == '2163902']
is_exist2 = info_post[info_post['poster_id'] == '2163902']
print(is_exist2['term_id'])
#990505,2163902,1822478,1618226,1997206,1669458,1015281413,10756151

#可以再试试别的不存在的poster_id
print('*************************************')
print('test3 start')
#查看term_id有几个
#253002 9003
print(info_post['term_id'].unique())
print(info_user['term_id'].unique())
#print(info_post['course_id'].unique())
print(info_user['course_id'].unique())
print('*************************************')
'''

#看看uid的作用
'''
wda_path = 'wda_mooc'
wda_name = 'wda_mooc_20001.txt'
wda_delim = '\t'
wda_data = read_data(wda_path,wda_name,wda_delim)
print(len(wda_data[0]))
print(len(wda_data))

for i in range(10):
    print(wda_data[i][22])
wda_col = ['logtime','login_type','filter','version','session_seq','hostname','character_set','screen_resolution','screen_color','language','flash_version','refer','url','os','browser','browser_version','uid','sid','first_session','last_session','current_session','ip','region','event_category','event_operation','event_label','daily_newuser','hourly_newuser','search_keyword','search_engine','referral','source','medium','utm_source','utm_medium','utm_campaign','custom_data','dt','type','url','refer']
#wda_col = 'logtime,login_type,filter,version,session_seq,hostname,character_set,screen_resolution,screen_color,language,flash_version,refer,url,os,browser,browser_version,uid,sid,first_session,last_session,current_session,ip,region,event_category,event_operation,event_label,daily_newuser,hourly_newuser,search_keyword,search_engine,referral,source,medium,utm_source,utm_medium,utm_campaign,custom_data,dt,type,url,refer']
wda_data = get_dataframe(wda_data,wda_col)
#编码貌似出了问题，utf-8不对？？？？？
wda_data.to_csv('wda.csv',encoding = 'utf-8')
print("write successfully!")
'''
starttime1 = datetime.now()
wda_data = pd.read_csv('wda.csv')
print("read successfully")
print(len(wda_data))
print(wda_data.ix[0])
print(wda_data.dtypes)
#??如何做到如下般的操作？
#print(wda_data[0:1,15])
#print(wda_data[0:1,16])
print(wda_data.info())
endtime1 = datetime.now()
print("method datetime() : %f s" % (endtime1 - starttime1).seconds)
#path = 'wda.csv'
#wda_data = np.array(wda_data)
#print("create array successfully")
#wda_data = np.delete(wda_data,22,axis = 0)
#print(len(wda_data[0]))
#print(wda_data[0])
#print("get narray successfully!")
#np.savetxt(path, wda_data,fmt = '%s',delimiter=',',header= wda_col, encoding = 'utf-8')
#print("write successfully!")
#wda_data = get_dataframe(wda_data,wda_col)
#print(len(wda_col))

'''
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
'''
'''
np.random.seed(42)  
a = np.random.randn(3,4)  
a[2][2] = np.nan  
print(a)
path = 'np.csv'
np.savetxt(path,a,fmt='%.2f',delimiter=',',header='#1,#2,#3,#4')
data = pd.read_csv(path)
print(data.info())
'''