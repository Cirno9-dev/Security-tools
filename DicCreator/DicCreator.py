from optparse import OptionParser

# 得到弱口令top100的列表
f = open('top100.txt','r')
tmp = f.readlines()
f.close()
top = []
for i in tmp:
    if '\n' in i :
        i = i.replace('\n','')
    top.append(i)

# 一个特殊符号
other1 = ['&','*','@','$','!','^','%','-','_','.']
# 两个特殊符号
other2 = []
for i1 in other1:
    for i2 in other1:
        other2.append(i1+i2)
# 三个特殊符号
other3 = []
for i1 in other2:
    for i2 in other1:
        other3.append(i1+i2)
# 特殊符号列表
other = [other1,other2,other3]

# 根据日期，得到日期列表
def create_date(date):
    datelist = []
    ymds = date.split(',')
    for ymd in ymds:
        y_m_d = ymd.split(':')
        datelist.append(y_m_d[0]+y_m_d[1]+y_m_d[2])
        datelist.append(y_m_d[0][2:]+y_m_d[1]+y_m_d[2])
        datelist.append(y_m_d[2]+y_m_d[1]+y_m_d[0])
        datelist.append(y_m_d[2]+y_m_d[1]+y_m_d[0][2:])
        datelist.append(y_m_d[1]+y_m_d[2]+y_m_d[0][2:])
        datelist.append(y_m_d[1]+y_m_d[2])
        datelist.append(y_m_d[2]+y_m_d[1])
    return datelist

# 得到关键词列表,并得到关键词全排列列表
def create_keywords(keywords):
    keywordslist = keywords.split(',')
    
    kwlist = keywordslist[:]
    kwlist_bak = kwlist[:]
    for _ in range(len(keywordslist)-1):
        for kw1 in kwlist_bak:
            for kw2 in keywordslist:
                if kw2 != kw1:
                    kwlist.append(kw1+kw2)
        kwlist_bak = kwlist[:]

    return kwlist

# 生成字典  
def generate(kwlist,datelist,top,other):
    print('Building dictionary...')

    f = open('password.txt','w')

    # 关键词及关键词排列直接写入
    for str1 in kwlist:
        f.write(str1+'\n')

    # 关键词排列加[1,2,3]特殊符号
    for str1 in kwlist:
        for str2list in other:
            for str2 in str2list:
                f.write(str1+str2+'\n')
    
    # top100
    for str1 in top:
        f.write(str1+'\n')

    # top100加[1,2,3]特殊符号
    for str1 in top:
        for str2list in other:
            for str2 in str2list:
                f.write(str1+str2+'\n') 

    # 关键词排列加top100 和 关键词排列加[1,2,3]特殊符号加top100
    for str1 in top:
        for str2 in kwlist:
            # 关键词排列加top100
            f.write(str1+str2+'\n')
            f.write(str2+str1+'\n')
            # 关键词排列加[1,2,3]特殊符号加top100
            for str3list in other:
                for str3 in str3list:
                    f.write(str1+str2+str3+'\n')
                    f.write(str1+str3+str2+'\n')
                    f.write(str2+str1+str3+'\n')
                    f.write(str2+str3+str1+'\n')

    # 若日期不为空
    if datelist != []:
        # 关键词排列加日期 和 关键词排列加日期加[1,2,3]特殊符号
        for str1 in kwlist:
            for str2 in datelist:
                # 关键词排列加日期
                f.write(str1+str2+'\n')
                f.write(str2+str1+'\n')
                # 关键词排列加日期加[1,2,3]特殊符号
                for str3list in other:
                    for str3 in str3list:
                        f.write(str1+str2+str3+'\n')
                        f.write(str1+str3+str2+'\n')
                        f.write(str2+str1+str3+'\n')
                        f.write(str2+str3+str1+'\n')
    f.close()

    # 输出总个数
    f = open('password.txt','r')
    num = len(f.readlines())
    f.close()
    print('The dictionary is generated, the total number is %d'%num)

if __name__ == "__main__":
    parse = OptionParser()
    parse.add_option('-D','--date',dest='date',help='Add a date(y:m:d),example:2020:01:10/2020:01:10,2020:11:25')
    parse.add_option('-K','--keywords',dest='keywords',help='Keywords which you get from the target,example:football/food,800225')
    parse.add_option('-N',dest='notop',action='store_true',help='Do not use the top100.txt')
    (options,args) = parse.parse_args()
    if options.keywords:
        datelist = []
        if options.date:
            datelist = create_date(options.date)
        
        if options.notop:
            top = []
        
        kwlist = create_keywords(options.keywords)
        generate(kwlist,datelist,top,other)
    else:
        parse.print_help()
        print('\nExample:')
        print('[#]-> python DicCreator.py -K 000322,ljx,github')
        print('[#]-> python DicCreator.py -D 2001:05:25 -K food')
        print('[#]-> python DicCreator.py -K ljx,github -N')
    pass