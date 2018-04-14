#开始正式对数据进行探索，用的多的尝试进行函数封装
'''
0.缩小所要用到的df(返回只有目标列的df，当然是全时间线上的，方便后续的groupby)
1.将数据进行时间划分的函数(真的需要专门的时间片划分吗？？#drop掉时间本来的数据，加上新列，或者说用replace那个)
2.获取用户是否退课这个标签(暂时没有按照蒲毅的定义)
3.将所有的time_data拼接起来的函数？
'''
import time
from datetime import datetime,timedelta
import numpy as np
import pandas as pd
from data_test5 import get_dataframe, read_data
#from log_feature_calculation import cal_time, unique_test, max_duration, cal_avg_interval_ddl

'''
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 500)
'''

def Valuefilling(data,process_column,source,target):
    #缺失值填充(限制在于要填充的列中的缺失值默认只用一个值来填充？当然要不这样其实也可以，那样list的元素可能还是一个list)
    #data 有缺失值的数据（dataframe）
    #process_column(list<str>)需要被替换的列的名称
    #source(list<list<>>) 需要被替换的值(谁是缺失值),一个元素也得是[[]]的形式！
    #target(list<list<>>) 替换上的值
    i = 0
    for x in process_column:
        data[x] = data[x].replace(source[i],target[i])
        i = i + 1
    return data



def log_Timesplit(data,start_time,end_time,duration,time_tag,time_last = 7,time_process = True):
    #先按照logtime切分时间片
    #后续还要用到logtime，所以会有些不一样

    #endtime是否多余
    #data(dataframe), merge完的数据
    #start_time(str)
    #end_time(str)
    #duration(week，str)
    #time_tag(str)——the column name related to time in data(used to split time)
    #time_last为时间粒度，此处用7天(一周)作为粒度
    #time_process用于判断是否要把13位的timestamp变成10位的
    #返回值
    #return timeseries list<dataframe>, 每个dataframe对应一周的数据(索引自增,不是时间戳，并且logtime这一datetime列还保留了，10位，在后续计算特征时有用)
    '''
    assumptions:
    1.start_time就等价于第一节课刚开始的时间(基本验证了)
    2.duration被认为week为单位的
    3.开课前的纪录+第一周的纪录被认为都是第一周的纪录(开课前记录也不能算！)
    4.最后一周的纪录 + 最后一周过后4周内的纪录被认为是最后一周的纪录
    5.余下的所有记录被剔除(未被返回)
    '''
    #定义返回值
    timeseries = []

    #怕是先转成int
    start_time = int(start_time)
    end_time = int(end_time)
    duration = int(duration)
    #如果starttime和endtime没有转化成datetime的数据，而是一个int的话，那么这里转化一下
    start_time = datetime.fromtimestamp(start_time//1000)
    end_time = datetime.fromtimestamp(end_time//1000)

    #0.时间这个位置上的可以先进行缺失值填充(用另一个函数)
    #!!!!时间项的缺失值一定要填充！(外部已经填充了)
    #!!!!user_tag_value中的时间如果要用的话,应该在函数外面自己进行转化，即str转为datetime(方法如下)，然后把time_process置为false
    #a[name] = pd.to_datetime(a[name])

    #先进行类型转化

    if time_process:
        #先把str型的转成int型的
        data[time_tag] = data[time_tag].astype('int')
        #数字型号的time要先转化成datetime(map)
        data[time_tag] = data[time_tag].map(lambda x : datetime.fromtimestamp(x//1000))
    
    #print("finish to get timestamp")
    #1.根据time_tag，将time_tag那一列设置成索引
    #print(data.head(10))
    data = data.set_index([time_tag])
    #（a.set_index(['timeset']),a['timeset']可以是str，但是不太好，因为索引类型时str不是datetime，可能并不方便一些切片操作）
    #2.是可以将time_tag这种index进行排序(升序)
    data = data.sort_index()
    #3.针对time_tag这种index来进行进行切分？(需要根据假设和传入的参数来划分时区)for循环？
    #print(data.head(10))


    for i in range(duration):
        #print("start to split " + str(i+1) + "weeks")
        begin_gap = timedelta(days = i*time_last)
        if i == duration - 1:
            finish_gap = timedelta(days = (i+4)*time_last)
        else:
            finish_gap = timedelta(days = (i+1)*time_last) 

        begin_time = start_time + begin_gap
        finish_time = start_time + finish_gap

        begin_time = begin_time.strftime('%Y-%m-%d')
        finish_time = finish_time.strftime('%Y-%m-%d')
        if i == 0:
        #第一周
            week_data = data[begin_time:finish_time]
        else:
        #正常情况
            week_data = data[begin_time:finish_time]
        #4.在3中不要忘记把切好的时间序列放进timeseries中去
        #print(week_data.head(10))
        #!!!添加之前需要把时间搞回来！
        week_data = week_data.reset_index()
        #把datatime转化为毫秒的那种？秒？(后续计算有用)
        #print("start to get timestamp")
        week_data[time_tag] = week_data[time_tag].map(lambda x : x.timestamp())#10位的
        #print(week_data.head(10))
        timeseries.append(week_data)

    return timeseries


def log_Usersplit_feature(log_data,usertag,term_id,timetag):
    #log_data为list,element是dataframe
    #log_data中应该确保没有nan(在开始的时候就搞定了)
    #usertag(str):用于groupby的那一列的列名(表明用户身份)
    #term_id:用于test筛选学期(str)，moc_test中读入的term_id应该就是str吧？
    #timetag(str):排序的时候用(升序)


    #返回值
    #user_log_feature:含有用户特征(times)的一个list<dataframe>(索引名不是uid)
    #user_label:含有用户标签的一个list<dataframe>(索引名不是uid)
    user_log_feature = []
    user_label = []
    column_name = ['uid','total_time','uni_test','sub_test','avg_sub_test','max_time','total_video_time','total_other_time','avg_gap']#需要提取的特征名称(暂时空缺)
    label_column = ['uid','label']

    #获取test的相关信息，用于user.generate_feature()
    f_path = 'moc_test'
    f_name = '000000_0'
    tests = read_data(f_path,f_name,'\x01')
    col_name = ['id', 'gmt_create', 'gmt_modified', 'release_time', 'name', 'description', 'test_time', 'trytime', 'analyse_setting', 'test_random_setting', 'type', 'term_id', 'chapter_id', 'deadline', 'subjective_total_score', 'objective_total_score', 'submit_test_count', 'score_pub_status', 'avg_score', 'exam_id', 'position_in_exam', 'oj_question_trytime', 'is_random']
    tests = get_dataframe(tests,col_name)
    #取相关学期的信息
    tests = tests[tests['term_id'] == term_id]
    tests = tests[['id','deadline']]#tests是个dataframe
    #ddl需要转化
    tests['deadline'] = tests['deadline'].astype('int')
    tests['deadline'] = tests['deadline'].map(lambda x : x//1000)
    #处理缺失值
    tests = tests.replace('-',np.nan)
    tests = tests.replace(r'\N',np.nan)
    tests = tests.replace('null',np.nan)
    tests = tests.replace('NULL',np.nan)
    tests = tests.replace('',np.nan)
    #删除有nan的行(id／ddl是nan)
    tests = tests.dropna()

    #对于每个dataframe进行单独处理
    for logpiece in log_data:
        #对其中的每个时间片,创建一个dataframe(空)
        week_data = pd.DataFrame(columns=column_name)
        week_data['sub_test'] = week_data['sub_test'].astype('float')
        week_data['avg_sub_test'] = week_data['avg_sub_test'].astype('float')
        #print(week_data.dtypes)
        week_label_data = pd.DataFrame(columns=label_column)
        week_label_data['label'] = week_label_data['label'].astype('int')
        #print(week_label_data.dtypes)
        for name, user_group in logpiece.groupby([usertag]):
            #name不必使用，但需要写
            #每个user_group都是一个dataframe(且保留了一致的user_tag)
            #先创建一个这个user的对象
            #print(user_group.index)
            #print(user_group.head(3))
            #print(type(user_group))
            #重置索引
            #进行一波排序？
            user_group = user_group.sort_values(by = timetag)
            #print(user_group.index)
            user_group = user_group.reset_index(drop = True)
            #print(user_group.index)
            #print(user_group.head(3))
            #print(type(user_group))
            #print(user_group.dtypes)
            user = User(user_group)
            #list(包含了uid，在首列)
            user_label_data, user_data = user.generate_feature(tests)
            #user_data为要插入的那一行(dataframe)
            
            user_data = pd.DataFrame([user_data], columns=column_name)
            user_label_data = pd.DataFrame([user_label_data], columns=label_column)
            week_data = week_data.append(user_data,ignore_index = True)#dataframe一定要赋值才行？list不必
            week_label_data = week_label_data.append(user_label_data,ignore_index = True)#dataframe一定要赋值才行？list不必
            
            #print(user_data.dtypes)
            #print(user_label_data.dtypes)
            #print(week_data.dtypes)
            #print(week_label_data.dtypes)
            
        #print(week_data.describe())
        user_log_feature.append(week_data)
        user_label.append(week_label_data)
    return user_label, user_log_feature


class User:
    def __init__(self,user_group):
        #只有重置了index才可以
        self.userid = user_group.ix[0,'uid']
        self.wda_list = self.get_wda_list(user_group)#list<Wda>,uid都相同
        self.all_actions = []
        self.video_actions = []
        self.do_test_actions = []#list<Wda>
        self.do_exam_actions = []
        self.other_actions = []
        for wda_info in self.wda_list:
            self.update(wda_info)

    def get_wda_list(self,user_group):
        list_wda = []
        for i in range(len(user_group)):#每个记录都变成了wda(获得了url_type,content之类的内容)
            current_wda = Wda(user_group.ix[i])
            list_wda.append(current_wda)
        return list_wda

    def update(self,wda_info):
        self.all_actions.append(wda_info)#所以all actions也必然是有序的了
        if wda_info.type == '1':
            self.video_actions.append(wda_info)
        elif wda_info.type == '2':
            self.do_test_actions.append(wda_info)
        elif wda_info.type == '3':
            self.do_exam_actions.append(wda_info)
        else:
            self.other_actions.append(wda_info)

    def generate_feature(self,test_list):
        #test_list是dataframe['id','deadline']
        #返回值是list(都含有userid)
        #user_feature:list
        #user_label:list

        user_feature = [self.userid]
        user_label = [self.userid]

        # generate feature
        # all actions
        #all_actions = self.video_actions + self.do_test_actions + self.do_exam_actions + self.other_actions
        #all_action.sort()???

        # total time spent on mooc
        total_time = cal_time(self.all_actions)
        # unique tests tried
        uni_test = unique_test(self.do_test_actions)
        # count of tests submit
        sub_test = len(self.do_test_actions)
        # avg submit of test
        if uni_test != 0:
            avg_sub_test = sub_test * 1.0 / uni_test
        else:
            avg_sub_test = 0
        # max duration of study
        max_time = max_duration(self.all_actions)
        # total time spent on videos
        total_video_time = cal_time(self.video_actions)
        # total time spend on other resources
        total_other_time = cal_time(self.other_actions)
        # avg time between test_ddl and submit time????
        avg_gap = cal_avg_interval_ddl(self.do_test_actions,test_list)
        # label : 0 for dropout, 1 for finish
        label = 0
        if len(self.do_exam_actions):#这个判定方式有点草率???
            label = 1
        else:
            label = 0
        user_feature.append(total_time)
        user_feature.append(uni_test)
        user_feature.append(sub_test)
        user_feature.append(avg_sub_test)
        user_feature.append(max_time)
        user_feature.append(total_video_time)
        user_feature.append(total_other_time)
        user_feature.append(avg_gap)
        user_label.append(label)
        #print(type(uni_test))
        #print(type(sub_test))
        #print(type(avg_sub_test))
        #print(type(avg_gap))
        #print(type(label))
        #print(user_feature.dtypes)
        #print(user_label.dtypes)
        return user_label,user_feature

#log_data中需要保留的列！？缺失值的列删除？(url处缺失的话)

#？？？wda_data中有用的属性：uid,sid,logtime,url，还有吗？(term_id和course_id的话日志中没有，但也没有必要)

#log_data = log_Timesplit(log_data, start_time, end_time, duration, 'logtime')#???

#？？？时间转化成小时为单位？或者分钟为单位？或者直接全体归一化吧

class Wda:
    def __init__(self,user_series):
        self.timestamp = user_series['logtime']
        #self.user_id = user_group.ix[wda_index,'uid']
        self.sid = user_series['sid']#session
        self.url = user_series['url.1']
        self.type, self.content = self.get_wda_type()

    def get_wda_type(self):
    #判断并记录每条记录对应的url的情况
        if 'content?type=detail&id=' in self.url:
            #视频
            type_info = self.url.split('content?type=detail&id=')[1]
            content = ''
            for ch in type_info:
                if ch >= '0' and ch <= '9':
                    content = content + ch
                else:
                    break
            return '1',content
        elif 'quiz?id=' in self.url:
            #test
            type_info = self.url.split('quiz?id=')[1]
            content = ''
            for ch in type_info:
                if ch >= '0' and ch <= '9':
                    content = content + ch
                else:
                    break
            return '2',content 
        elif 'examSubjective?eid=' in self.url:
            #exam
            type_info = self.url.split('examSubjective?eid=')[1]
            content = ''
            for ch in type_info:
                if ch >= '0' and ch <= '9':
                    content = content + ch
                else:
                    break
            return '3',content 
        else:
            #others
            return '-1', '-1'    

def Userfeature_Process(user_log_feature, user_tag, term_id):
    #对于user_log_feature要做一些预处理
    #必须要每个时间段都和user_tag_value merge一把
    #user_log_feature为list,element是dataframe
    #user_tag(str):表明用户id的那一列的列名
    #new_user_features:list<dataframe>  返回值，预处理成功的user_feature(索引名是user_id!!!!)
    #term_id:user_tag_value的话需要term_id来筛选一下(在merge之前)
    #删除重复列(确保user_tag不叫'user_id'!!)

    #获取user的list
    user_name = 'user_tag_value'
    user_info = []
    for i in range(37):
        if i < 10:
            user_path = user_name + '/' + '00000'+str(i)+'_0'
        else:
            user_path = user_name + '/' + '0000' + str(i)+'_0'
        with open(user_path,'r',encoding = 'utf-8') as f:
            temp_info = f.readlines()
            delim = '\x01'
            for line in temp_info: 
                user_info.append(line.strip().split(delim))
    #print("用户记录总数" + str(len(user_info)))

    #获取user的dataframe
    user_col = ['user_id','nickname','birthday','sex','region','last_time_in_mooc','course_id','term_id','choose_time']
    user_info = get_dataframe(user_info,user_col)

    full_user_id = user_info[user_info['term_id'] == term_id]
    full_user_id = full_user_id[['user_id','birthday']]

    #缺失值（防止user_id中有缺失值）
    full_user_id = full_user_id.replace('-',np.nan)
    full_user_id = full_user_id.replace('NULL',np.nan)
    full_user_id = full_user_id.replace('',np.nan)
    full_user_id = full_user_id.replace(r'\N',np.nan)
    full_user_id = full_user_id.replace('null',np.nan)
    full_user_id['birthday'] = full_user_id['birthday'].replace(np.nan,'00000')
    full_user_id = full_user_id.dropna()

    #print(type(full_user_id))
    #print(len(full_user_id))
    #print(full_user_id.describe())
    #开始merge
    new_user_feature = []
    for feature_piece in user_log_feature:
        #print(type(feature_piece))
        feature_piece = pd.merge(full_user_id,feature_piece,left_on = 'user_id',right_on = user_tag, how = 'left')
        feature_piece.pop('birthday')
        #删除重复列(确保user_tag不叫'user_id'!!)
        feature_piece.pop(user_tag)#此列有nan的也一起弹出了
        #对merge造成的nan的话进行填充0(很合理)
        feature_piece = feature_piece.replace(np.nan,0)
        #重置索引名
        feature_piece = feature_piece.set_index('user_id')
        new_user_feature.append(feature_piece)
    return new_user_feature

def cal_time(actions):
    #actions:list<Wda>
    #!!!!预先排序的重要性
    action_time = 0.0
    if len(actions) < 2:
        #只有一条记录或者没有
        return action_time
    presession = actions[0].sid
    pretimestamp = actions[0].timestamp
    for action in actions[1:]:
        #所有连续时间的总和
        if action.sid == presession:
            action_time = action_time + action.timestamp - pretimestamp
        pretimestamp = action.timestamp
        presession = action.sid
    return action_time

def unique_test(actions):
    #actions是list<Wda>
    test_times = 0.0
    #集合具有不重复性！
    tests = set()
    for action in actions:
        if action.type == '2' and action.content not in tests:
            tests.add(action.content)
            test_times = test_times + 1
    return test_times

def max_duration(actions):
    #actions是list<Wda>
    max_time = 0.0
    if len(actions) < 2:
        return max_time
    presession = actions[0].sid
    pretimestamp = actions[0].timestamp
    for action in actions[1:]:
        if action.sid == presession:
            max_time = max(max_time, action.timestamp - pretimestamp)
        else:
            pretimestamp = action.timestamp
            presession = action.sid
    return max_time

def cal_avg_interval_ddl(actions, test_list):
    #actions是list<Wda>
    #test_list是dataframe['id','deadline']
    ad_time = 0.0
    total_time = 0.0
    for action in actions:
        if action.type == '2':
            temp = test_list[(test_list['id'] == action.content) & (test_list['deadline'] > action.timestamp)]
            if temp.empty == False:#非空(存在同一个test多次ddl的可能？讲道理不可能，即使可能，下面的计算也不科学了，action.stamp只是一个值)
                #temp是dataframe
                #temp变成了seires???
                temp = temp.reset_index(drop = True)
                for i in range(len(temp)):
                    ad_time = ad_time + temp.ix[i,'deadline'] - action.timestamp
                    total_time = total_time + 1
    if total_time == 0:
        return 0.0
    else:
        return ad_time * 1.0 /total_time
