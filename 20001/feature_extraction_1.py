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
'''
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 500)


print('test4 start:moc_reply')
f_path = 'moc_reply'
f_name = '000000_0'
info = read_data(f_path,f_name,'\x01')
print("the number of elements in each record : %d " % len(info))
print(info[0])
#print("the number of elements in col_name : %d" % len(col_name))
#删去对不上的content
col_name = ['id', 'gmt_create', 'gmt_modified', 'replyer_id', 'anonymous', 'post_id', 'count_vote', 'count_comment', 'reply_time', 'deleted', 'tag_agree', 'tag_top', 'tag_top_time', 'active_flag', 'forum_id', 'term_id']
info = get_dataframe(info, col_name)


#查看数据大致信息
print(info.describe())
print(info.dtypes)
print(info.info())

info['gmt_create'] = info['gmt_create'].astype('int')
print("type ok")
print(info.dtypes)
info['gmt_create'] = info['gmt_create'].map(lambda x : datetime.fromtimestamp(x//1000))
print(info.ix[0,'gmt_create'])
datetime_str = info.ix[0,'gmt_create'].strftime('%Y-%m-%d')
print(datetime_str)
print(type(datetime_str))
print(info.dtypes)

'''

'''
0 返回只有目标列的这个事情不需要函数自己做就可以，需要的名称构成一个list，然后赋值就行

  
  每个表转化成dataframe的时候内部的数据结构自己要清楚！！！
  (都是object吧，如果自己要输出一个wda.csv的话可能会有变化，但是可能是因为之前的dataframe就已经转化了？？？？)  

  还有就是每一列的缺失值填充的问题，弄清楚该列所表示的缺失值是什么，目前貌似user_tag_value是 '\\N' 其他都是pd.nan？
  (善于使用replace)

  类型转换的问题，尤其是一些关键列的类型一定要转化或者确保正确(),merge的时候对应的列也是!!!(类型都不对肯定要merge失败)
  merge之后的drop问题？？？？

  user_tag_value中merge的时候一些在课程结束时间之后选课的人应该就剔除的！(如何剔除某一行数据呢？因为user_tag_value并不是index)
  （讲道理这类人应该也就没有之前时间）

  是否需要排序？排序结果不改变index，除非reset_index


  ？？？是否应该做一些统计图？ 热力图（活动的），根据周次？？？
  某些统计量的获取，课程一共有多少注册用户，除去没有任何活动的有多少？(非全零的？可以通过最后一次登陆mooc时间来看吗？但是这个登陆mooc时间真的是该门课程吗？)
  
  用户都是选了这门课的用户

  user_tag_value中course_id和term_id搞混的

  清楚特征全零的用户？ 每次merge时user_tag_value中的用户都需要全部保留，缺失值填充策略？？？(至少用户id处是没有缺失值的)
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


#1
#??time这个问题貌似还没验证呢！！！！
def Timesplit(data,start_time,end_time,duration,time_tag,time_last = 7,time_process = True):

    #endtime是否多余(貌似是)
    #data(dataframe，默认其中的time数据是str且为时间戳), merge完的数据
    #start_time(str)
    #end_time(str)
    #duration(week，str)
    #time_tag(str)——the column name related to time in data(used to split time)
    #timedata应该是一个df构成的list?!
    #time_last为时间粒度，此处用7天(一周)作为粒度
    #return 一个list， element为dataframe, 每个dataframe对应一周的数据
    '''
    assumptions:
    1.start_time就等价于第一节课刚开始的时间(基本验证了)
    2.duration被认为week为单位的
    3.开课前的纪录+第一周的纪录被认为都是第一周的纪录(虽然没验证过是否真的有人开课前就有记录,开课前记录也不能算！)
    4.最后一周的纪录 + 最后一周过后4周内的纪录被认为是最后一周的纪录
    5.余下的所有记录被剔除(未被返回)
    '''
    #定义返回值
    timeseries = []

    #先转成int
    start_time = int(start_time)
    end_time = int(end_time)
    duration = int(duration)
    #如果starttime和endtime没有转化成datetime的数据，而是一个int的话，那么这里转化一下
    start_time = datetime.fromtimestamp(start_time//1000)
    end_time = datetime.fromtimestamp(end_time//1000)

    #0.时间这个位置上的可以先进行缺失值填充(用另一个函数)
    #!!!!时间项的缺失值一定要填充！
    #!!!!user_tag_value中的时间如果要用的话,应该在函数外面自己进行转化，即str转为datetime(方法如下)，然后把time_process置为false
    #a[name] = pd.to_datetime(a[name])
    #先进行类型转化

    #先把str型的转成int型的
    data[time_tag] = data[time_tag].astype('int')
    # 数字型号的time要先转化成datetime(map)
    if time_process:
        data[time_tag] = data[time_tag].map(lambda x : datetime.fromtimestamp(x//1000))
    #1.根据time_tag，将time_tag那一列设置成索引
    data = data.set_index([time_tag])
    #（a.set_index(['timeset']),a['timeset']可以是str，但是不太好，因为索引类型时str不是datetime，可能并不方便一些切片操作）
    #2.是可以将time_tag这种index进行排序吧？(升序)
    data = data.sort_index()
    #3.针对time_tag这种index来进行进行切分？(需要根据假设和传入的参数来划分时区)for循环？
    
    for i in range(duration):
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
        timeseries.append(week_data)

    return timeseries


def Usersplit_times(timeseries,usertag):
    #!!!暂时只是统计的次数！
    #timeseries为list,element是dataframe
    #!!!!timeseries中应该确保没有nan(不能因为一些莫名其妙的属性来影响该列的存在，不利于size的计算)
    #usertag(str):用于groupby的那一列的列名(表明用户身份)

    #返回值
    #user_feature:含有用户特征(times)的一个list<dataframe>，是返回值(索引不是user_id)
    user_feature = []
    #对于每个dataframe进行单独处理(索引是time)
    for timepiece in timeseries:
        #去除时间索引吧(赋值！)
        timepiece = timepiece.reset_index(drop = True)
        #groupby
        timepiece = timepiece.groupby([usertag]).size()
        timepiece = timepiece.reset_index()#series转变为dataframe
        user_feature.append(timepiece)
    return user_feature

def Usersplit_sum(timeseries,usertag,sum_tag):
    #!!!暂时只是统计的次数！
    #timeseries为list,element是dataframe
    #!!!!timeseries中应该确保没有nan(不能因为一些莫名其妙的属性来影响该列的存在，不利于size的计算)
    #usertag(str):用于groupby的那一列的列名(表明用户身份)
    #sum_tag:用于计算sum的那一列(str)

    #返回值
    #user_feature:含有用户特征(times)的一个list<dataframe>，是返回值(索引不是user_id)
    user_feature = []
    #对于每个dataframe进行单独处理(索引是time)
    for timepiece in timeseries:
        #去除时间索引吧(赋值！)
        timepiece = timepiece.reset_index(drop = True)
        #groupby        
        #timepiece = timepiece.groupby([usertag]).size()
        timepiece = timepiece.groupby([usertag])[sum_tag].sum()
        timepiece = timepiece.reset_index()#series转变为dataframe
        user_feature.append(timepiece)
    return user_feature



#想法有误，应该先groupby之后再和user_tag_value合并
def Userfeature_Process(user_feature, user_tag,term_id):
    #对于user_feature要做一些预处理
    #必须要每个时间段都和user_tag_value merge一把
    #user_feature为list,element是dataframe
    #usertag(str):表明用户id的那一列的列名
    #new_user_features:list<dataframe>  返回值，预处理成功的user_feature(索引名是user_id)
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
    full_user_id = full_user_id.replace(r'\N',np.nan)
    full_user_id = full_user_id.replace('null',np.nan)
    full_user_id = full_user_id.replace('NULL',np.nan)
    full_user_id = full_user_id.replace('',np.nan)
    full_user_id['birthday'] = full_user_id['birthday'].replace(np.nan,'00000')
    full_user_id = full_user_id.dropna()
    #print(type(full_user_id))
    #print(len(full_user_id))
    #print(full_user_id.describe())
    #开始merge
    new_user_feature = []
    for feature_piece in user_feature:
        #print(type(feature_piece))
        feature_piece = pd.merge(full_user_id,feature_piece,left_on = 'user_id',right_on = user_tag, how = 'left')
        feature_piece.pop('birthday')
        #删除重复列(确保user_tag不叫'user_id'!!)
        feature_piece.pop(user_tag)#此列有nan的也一起弹出了
        #对merge造成的nan的话进行填充0
        feature_piece = feature_piece.replace(np.nan,0)
        #重置索引名(方便后续concat)
        feature_piece = feature_piece.set_index('user_id')
        new_user_feature.append(feature_piece)
    return new_user_feature


def feature_concact(user_feature1,user_feature2):
   #将各个特征的表合并成一个dataframe,但还是按周划分
   #应该是传入的参数都经历过了userfeature_process才行(每个特征每周都是全量的用户且index是用户名)
   #user_feature1:list<dateframe>,(索引名是user_id)
   #user_feature2:list<dateframe>,(索引名是user_id)
   #user_features:返回值，list<dateframe> (索引名是user_id)
   user_features = []
   for i in range(len(user_feature1)):
       #对每一周的数据进行处理
       temp_features = pd.concat([user_feature1[i],user_feature2[i]],axis = 1)
       user_features.append(temp_features)
   return user_features


def week_concact(user_features):
    #user_features:list<dataframe>,(索引名是user_id)
    #user_data:dataframe,(索引名不是user_id，重置了！)
    user_data = user_features[0]
    #添加'\t',便于转化成list
    col_name = 'del_0'
    user_data[col_name] = '\t'
    loop = len(user_features) - 1
    for i in range(loop):
        #两两合并
        user_data = pd.concat([user_data,user_features[i+1]],axis = 1)
        if i < loop - 1:
           #不是最后一次合并的话，手动添加‘\t’
           col_name = 'del_' + str(i+1)
           user_data[col_name] = '\t'
    #把用户名放入了第一列中！(恢复原位)
    user_data.reindex()
    return user_data

def get_listdata(user_data):
    #将dataframe转化为list
    #user_data为dataframe
    #list_data为list<list>(方便后续写入文件)，每个元素对应一个用户的数据（userid,feature1……）
    #！！！方便转化的话，现将所有的内容都变成str类型
    user_data = user_data.astype('str')
    list_data = user_data.values
    list_data = list_data.tolist()
    return list_data


def w_list_txt(list_data,filename):
    #记住输出换行！！！
    with open(filename,'w',encoding = 'utf-8') as f:
        for list in list_data:#每个用户的特征
            for element in list:
                f.write(element)
                if(element != '\t'):#每周特征的间隔符
                    f.write(' ')
            f.write('\n')
    return