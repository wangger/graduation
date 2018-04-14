#主要测试一下读取的速度
#一门课总共100+m，此处先读去一个4.8m(需要循环)的试下，后续再读去一个100+m的
#split()返回list（[]）
#4.8m秒读的!
#结果：用户记录书——55591
F_PATH = "user_tag_value"
user_infos = []
for val in range(37):
    if val < 10:
        F_NAME = '00000'+str(val)+'_0'
    else:
        F_NAME = '0000'+str(val)+'_0'
    FILE_NAME = F_PATH +'/'+F_NAME
    with open(FILE_NAME, 'r', encoding = 'utf-8') as f:
        temp_infos = f.readlines()#已经是一个list
        for temp_info in temp_infos:
            delim = '\x01'
            user_infos.append(temp_info.strip().split(delim))
            #print(user_infos[-1])
print("用户记录总数" + str(len(user_infos)))


'''
test = [[1, 1, 1, 1], [2, 2, 2, 2]]
print("test:" + str(len(test)))
'''
print("END")
