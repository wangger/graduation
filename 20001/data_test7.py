#开始正式对！！！！wda的数据进行探索，用的多的尝试进行函数封装

#探索每个表的数据和表之间的联系
'''
experiments
1.user_tag_value表中的每列信息，decribe()一波，所有人都是选了一门课吗？
'''

'''
answer
1.??重复出现的user_id不知什么情况
'''

import time
from datetime import datetime
import numpy as np
import pandas as pd
from data_test5 import get_dataframe, read_data

#np.set_printoptions(threshold = np.inf)
#np.set_printoptions(threshold='nan')
#为了方便显示
pd.set_option('display.max_columns',None)
pd.set_option('display.max_colwidth',500)
'''
print('test1 start:user_tag_value')
#读取数据
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
print("用户(记录)总数" + str(len(user_infos)))
#用户信息也要转化为dataframe
user_col = ['user_id','nickname','birthday','sex','region','last_time_in_mooc','term_id','course_id','choose_time']
user_infos = get_dataframe(user_infos,user_col)
#查看数据大致信息
print(user_infos.describe())
print(user_infos.dtypes)
print(user_infos.info())
print('*************************************')
'''
'''
print('test2 start:moc_post')
#删去对不上的term_id
f_path = 'moc_post'
f_name = '000000_0'
infos = read_data(f_path,f_name,'\x01')
print(infos[0])
print("the number of elements in each record : %d " % len(infos[0]))
col_name = ['id','gmt_create','gmt_modified','type','lesson_unit_id','forum_id','root_forum_id','term_id','poster_id','post_time','title','last_replyer','last_reply_time','anonymous','tag_agree','tag_top','tag_top_time','tag_solve','tag_lector','count_browse','count_reply','count_vote','deleted','active_flag','lock_flag']
print("the number of elements in col_name : %d" % len(col_name))
infos = get_dataframe(infos,col_name)
#查看数据大致信息
print(infos.describe())
print(infos.dtypes)
print(infos.info())
print('*************************************')
'''
'''
print('test3 start:moc_post_detail')
#删去对不上的term_id
#读取数据
post_path = 'moc_post_detail'
post_infos = []
for val in range(2):
    post_name = '00000'+str(val)+'_0'
    post_filename = post_path + '/' + post_name
    with open(post_filename, 'r', encoding = 'utf-8') as f:
        temp_infos = f.readlines()
        for temp_info in temp_infos:
            post_infos.append(temp_info.strip().split('\x01'))
print("post(记录)总数" + str(len(post_infos)))
#用户信息也要转化为dataframe
post_col = ['id','gmt_create','gmt_modified','content']
post_infos = get_dataframe(post_infos,post_col)
#查看数据大致信息
print(post_infos.describe())
print(post_infos.dtypes)
print(post_infos.info())
print('*************************************')
'''
'''
print('test4 start:moc_reply')
f_path = 'moc_reply'
f_name = '000000_0'
info = read_data(f_path,f_name,'\x01')
print("the number of elements in each record : %d " % len(info))
print(info[0])
col_name = ['id', 'gmt_create', 'gmt_modified', 'replyer_id', 'anonymous', 'post_id', 'content', 'count_vote', 'count_comment', 'reply_time', 'deleted', 'tag_agree', 'tag_top', 'tag_top_time', 'active_flag', 'forum_id', 'term_id'
]
#print("the number of elements in col_name : %d" % len(col_name))
#删去对不上的term_id
col_name = ['id', 'gmt_create', 'gmt_modified', 'replyer_id', 'anonymous', 'post_id', 'count_vote', 'count_comment', 'reply_time', 'deleted', 'tag_agree', 'tag_top', 'tag_top_time', 'active_flag', 'forum_id', 'term_id']
info = get_dataframe(info,col_name)

#查看数据大致信息
print(info.describe())
print(info.dtypes)
print(info.info())
print('*************************************')
'''
'''
print('test4 start:moc_comment')
f_path = 'moc_comment'
f_name = '000000_0'
info = read_data(f_path,f_name, '\x01')
print("the number of elements in each record : %d " % len(info))
print(info[0])
col_name = ['id', 'gmt_create', 'gmt_modified', 'commentor_id', 'anonymous', 'post_id', 'reply_id', 'count_vote', 'comment_time', 'deleted', 'tag_agree', 'tag_top', 'tag_top_time', 'active_flag', 'forum_id', 'term_id']
info = get_dataframe(info,col_name)
#查看数据大致信息
print(info.describe())
print(info.dtypes)
print(info.info())
print('*************************************')
'''
'''
print('test4 start:moc_mutual_evaluate')
post_path = 'moc_mutual_evaluate'
post_infos = []
for val in range(2):
    post_name = '00000'+str(val)+'_0'
    post_filename = post_path + '/' + post_name
    with open(post_filename, 'r', encoding = 'utf-8') as f:
        temp_infos = f.readlines()
        for temp_info in temp_infos:
            post_infos.append(temp_info.strip().split('\x01'))
print("evaluate(记录)总数" + str(len(post_infos)))
#用户信息也要转化为dataframe
post_col = ['id','gmt_create','gmt_modified','evaluator_id','test_answerer_id','test_id','answerform_id','status','orig_score','evaluate_judge_type']
post_infos = get_dataframe(post_infos,post_col)
#查看数据大致信息
print(post_infos.describe())
print(post_infos.dtypes)
print(post_infos.info())
print('*************************************')
'''
'''
print('test5 start:moc_mutaul_evaluate_detail')
post_path = 'moc_mutual_evaluate_detail'
post_infos = []
for val in range(8):
    post_name = '00000'+str(val)+'_0'
    post_filename = post_path + '/' + post_name
    with open(post_filename, 'r', encoding = 'utf-8') as f:
        temp_infos = f.readlines()
        for temp_info in temp_infos:
            post_infos.append(temp_info.strip().split('\x01'))
print("evaluate_detail(记录)总数" + str(len(post_infos)))
#用户信息也要转化为dataframe
post_col = ['id','gmt_create','gmt_modified','test_id','evaluate']
post_infos = get_dataframe(post_infos,post_col)
#查看数据大致信息
print(post_infos.describe())
print(post_infos.dtypes)
print(post_infos.info())
print('*************************************')
'''
'''
print('test6 start: moc_course')
f_path = 'moc_course'
f_name = '000000_0'
info = read_data(f_path,f_name, '\x01')
print("the number of elements in each record : %d " % len(info))
print(info[0])
col_name = ['id','gmt_create','gmt_modified','name','school_id','status','current_term_id','start_time','duration','end_time','first_publish_time','course_load','big_photo','short_name','video_id','train_id','web_visible','weight','mode','channel','from_course_id','support_oj',             'previous_courses','from_course_mode','origin_copy_right_course_id','apply_mooc_status','current_term_chargeable']
info = get_dataframe(info,col_name)
#查看数据大致信息
print(info.ix[0])
info = info.dropna()
print('after drop')
print(info.ix[0])
print(info.describe())
print(info.dtypes)
print(info.info())
print('*************************************')
'''

'''
print('test7 start: moc_term')
f_path = 'moc_term'
f_name = '000000_0'
info = read_data(f_path,f_name, '\x01')
print("the number of elements in each record : %d " % len(info))
#print(info[0])
col_name = ['id','gmt_create','gmt_modified','course_id','start_time','duration','end_time','publish_status','small_photo','big_photo','course_load','first_publish_time','close_visable_status','web_visible','achievement_status','term_no','chargeable_cert','achievement_confirmed_time','time_to_freeze','mode','from_term_id','school_id','password','qualified_count','excellent_count','enroll_count','delta_start','delta_end','weight_total','weight_starting','weight_started','weight_finished','origin_copy_right_term_id','apply_mooc_status','from_term_mode','uniform_combo_score',  'mob_uniform_combo_score','copied','copy_time','price']
info = get_dataframe(info,col_name)
#查看数据大致信息
print(info.ix[0])
starttime = datetime.fromtimestamp(int(info.ix[0,'start_time'])//1000)
endtime = datetime.fromtimestamp(int(info.ix[0,'end_time'])//1000)
first_pub_time = datetime.fromtimestamp(int(info.ix[0,'first_publish_time'])//1000)
gmt_cre = datetime.fromtimestamp(int(info.ix[0,'gmt_create'])//1000)
gmt_mod = datetime.fromtimestamp(int(info.ix[0,'gmt_modified'])//1000)
ac_time = datetime.fromtimestamp(int(info.ix[0,'achievement_confirmed_time'])//1000)
fre_time = datetime.fromtimestamp((int(info.ix[0,'end_time']) + int(info.ix[0,'time_to_freeze']))//1000)
delta_start = datetime.fromtimestamp((int(info.ix[0,'delta_start']) + int(info.ix[0,'start_time']))//1000)
delta_end = datetime.fromtimestamp((int(info.ix[0,'end_time']) + int(info.ix[0,'delta_end']))//1000)
print(starttime)
print(endtime)
print(first_pub_time)
print(gmt_cre)
print(gmt_mod)
print(ac_time)
print(fre_time)
print(delta_start)
print(delta_end)

#print(info.describe())
#print(info.dtypes)
#print(info.info())
print('*************************************')
'''
'''
print('test8 start: moc_lesson')
f_path = 'moc_lesson'
f_name = '000000_0'
info = read_data(f_path,f_name, '\x01')
print("the number of elements in each record : %d " % len(info))
print(info[48])
col_name = ['id','gmt_create','gmt_modified','name','position','release_time','term_id','chapter_id','content_type','content_id']
info = get_dataframe(info,col_name)
#查看时间信息
gmt_cre = datetime.fromtimestamp(int(info.ix[49,'gmt_create'])//1000)
gmt_mod = datetime.fromtimestamp(int(info.ix[49,'gmt_modified'])//1000)
release_time = datetime.fromtimestamp(int(info.ix[49,'release_time'])//1000)
print(gmt_cre)
print(gmt_mod)
print(release_time)

#查看数据大致信息
print(info.describe())
print(info.dtypes)
print(info.info())
print('*************************************')
'''

'''
print('test9 start: moc_lesson_unit')
f_path = 'moc_lesson_unit'
f_name = '000000_0'
info = read_data(f_path,f_name, '\x01')
print("the number of elements in each record : %d " % len(info))
print(info[0])
col_name = ['id','gmt_create','gmt_modified','name','position','lesson_id','chapter_id','term_id','content_type', 'content_id','json_content']
info = get_dataframe(info,col_name)
#查看数据大致信息
print(info.describe())
print(info.dtypes)
print(info.info())
print('*************************************')
'''
#print('test10 start: moc_lesson_unit')


#？？（moc_lesson_unit_content?）

'''
print('test9 start: moc_lesson_unit')
f_path = 'moc_test'
f_name = '000000_0'
info = read_data(f_path,f_name,'\01')
col_name = ['id', 'gmt_create', 'gmt_modified', 'release_time', 'name', 'description', 'test_time', 'trytime', 'analyse_setting', 'test_random_setting', 'type', 'term_id', 'chapter_id', 'deadline', 'subjective_total_score', 'objective_total_score', 'submit_test_count', 'score_pub_status', 'avg_score', 'exam_id', 'position_in_exam', 'oj_question_trytime', 'is_random']
info = get_dataframe(info,col_name)
#查看数据大致信息
print(info.ix[0])
print(info.describe())
print(info.dtypes)
print(info.info())
print('*************************************')

'''
print('test10 start: moc_test')
f_path = 'moc_test'
f_name = '000000_0'
info = read_data(f_path,f_name,'\01')
col_name = ['id', 'gmt_create', 'gmt_modified', 'release_time', 'name', 'description', 'test_time', 'trytime', 'analyse_setting', 'test_random_setting', 'type', 'term_id', 'chapter_id', 'deadline', 'subjective_total_score', 'objective_total_score', 'submit_test_count', 'score_pub_status', 'avg_score', 'exam_id', 'position_in_exam', 'oj_question_trytime', 'is_random']
# 'id', 'gmt_create', 'gmt_modified', 'release_time', 'name,description', 'test_time', 'trytime', 'analyse_setting', 'test_random_setting', 'type,term_id', 'chapter_id', 'deadline', 'subjective_total_score', 'objective_total_score', 'submit_test_count', 'score_pub_status', 'avg_score', 'exam_id','position_in_exam', 'oj_question_trytime', 'is_random' 
info = get_dataframe(info,col_name)
#查看数据大致信息
print(info.ix[0])
print(info.describe())
print(info.dtypes)
print(info.info())
print('*************************************')