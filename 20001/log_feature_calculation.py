import time
from datetime import datetime,timedelta
import numpy as np
import pandas as pd
from data_test5 import get_dataframe, read_data
#from process_log import *#???

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 500)



def cal_time(actions):
    #actions:list<Wda>
    #!!!!预先排序的重要性
    action_time = 0
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
    test_times = 0
    #集合具有不重复性！
    tests = set()
    for action in actions:
        if action.type == 2 and action.content not in tests:
            tests.add(action.content)
            test_times = test_times + 1
    return test_times

def max_duration(actions):
    #actions是list<Wda>
    max_time = 0
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
    ad_time = 0
    total_time = 0
    for action in actions:
        if action.type == 2:
            temp = test_list[(test_list['id'] == action.content) & (test_list['deadline'] > action.timestamp)]
            if temp.empty == False:#非空(存在同一个test多次ddl的可能？讲道理不可能，即使可能，下面的计算也不科学了，action.stamp只是一个值)
                #temp是dataframe
                for i in range(len(temp)):
                    ad_time = ad_time + temp.ix[i,'deadline'] - action.timestamp
                    total_time = total_time + 1
    if total_time == 0:
        return 0
    else:
        return ad_time * 1.0 /total_time
