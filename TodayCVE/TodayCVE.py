import requests
import re
from bs4 import BeautifulSoup
import json
import os
import sqlite3
import time
from optparse import OptionParser

def getCVEurl():
    #定义headers
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding':'gzip, deflate',
        'Upgrade-Insecure-Requests':'1',
    }
    url = 'https://cassandra.cerias.purdue.edu/CVE_changes/today.html'

    html = requests.get(url, headers=headers)
    txt = html.text
    #得到url所在区间
    start = 'New entries:'
    end = 'Graduations'
    start_index = txt.index(start)
    end_index = txt.index(end)
    target = txt[start_index:end_index]
    #得到时间所在区间
    start = 'date: '
    end = 'New entries:'
    start_index = txt.index(start)
    end_index = txt.index(end)
    time_html = txt[start_index:end_index]
    #正则匹配时间
    time = re.findall("date: (.*)<BR>",time_html)
    #正则匹配url和编号
    cveurls = re.findall('<A HREF = \'(.*)\'>(.*)</A>',target)
    return time,cveurls

def getCVEinfo(cveurl):
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding':'gzip, deflate',
        'Upgrade-Insecure-Requests':'1',
    }
    html = requests.get(cveurl,headers=headers)
    txt = html.text
    soup = BeautifulSoup(txt,'lxml')
    #找到描述所在区间，并得到描述
    table = soup.find("div",id='GeneratedTable').find("table")
    cve_description = table.find_all("tr")[3].find("td").string
    if cve_description:
        return cve_description
    else:
        return "None"

def getTranslation(text):
    if text == "None":
        return "None"
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding':'gzip, deflate',
        'Upgrade-Insecure-Requests':'1',
    }
    #调用Google翻译，来对英文描述进行翻译
    url = "https://translate.google.cn/translate_a/single?client=gtx&sl=en&tl=zh-CN&dt=t&q="+text
    jsondata = json.loads(requests.get(url,headers=headers).text)
    translation = ""
    for data in jsondata[0]:
        translation += data[0]
    return translation

#创建数据库
def initCVEdb():
    conn = sqlite3.connect("CVE.db")
    createsql = """Create Table IF NOT EXISTS CVEinfo (
        date TEXT,
        CVEId TEXT,
        URL TEXT,
        description_En TEXT,
        description_Zh TEXT)"""
    conn.execute(createsql)
    conn.commit()
    conn.close()

#判断今天是否已经写入,并将存在的进行输出，减少requests的次数
def checkToday(date):
    conn = sqlite3.connect("CVE.db")
    conn.isolation_level = None
    cur = conn.cursor()
    cur.execute('SELECT * FROM CVEinfo WHERE date='+'\''+date+'\'')
    res = cur.fetchall()
    conn.close()
    for data in res:
        print("\033[32m[+]\033[0m "+data[1])
        print("\033[32m[+]\033[0m Url : "+data[2])
        print("\033[32m[+]\033[0m Description-En : "+data[3])
        print("\033[32m[+]\033[0m Description-Zh : "+data[4]+"\n")
    return len(res)

#将CVE数据写入数据库中
def writeCVEdb(date,CVEId,url,description_En,description_Zh):
    conn = sqlite3.connect("CVE.db")
    conn.isolation_level = None
    cur = conn.cursor()
    cur.execute("INSERT INTO CVEinfo (date,CVEId,URL,description_En,description_Zh) VALUES(\"{}\",\"{}\",\"{}\",\"{}\",\"{}\")".format(date,CVEId,url,description_En,description_Zh))
    conn.close()

def update():
    print("Hello!")
    os.system("whoami")
    print("数据来源:https://cassandra.cerias.purdue.edu/CVE_changes/today.html")
    print("每天17:02网站更新漏洞.\n")
    today,cveurls = getCVEurl()
    #输出时间
    print("\t\t"+today[0])
    print("="*50)
    #判断是否存在数据库以及今天是否已经写入
    if not os.path.exists("CVE.db"):
        initCVEdb()
    flag = checkToday(today[0])
    #输出url和编号,描述和中文翻译
    for i in range(flag,len(cveurls)):
        print("\033[32m[+]\033[0m CVE-"+cveurls[i][1])
        print("\033[32m[+]\033[0m Url : "+cveurls[i][0])
        description_En = getCVEinfo(cveurls[i][0]).replace("\"","\'")
        print("\033[32m[+]\033[0m Description-En : "+description_En.strip())
        description_Zh = getTranslation(description_En.strip()).replace("\"","\'")
        print("\033[32m[+]\033[0m Description-Zh : "+description_Zh.strip()+"\n")
        writeCVEdb(today[0],"CVE-"+cveurls[i][1],cveurls[i][0],description_En.strip(),description_Zh.strip())
        #暂停，防止Google翻译对IP进行限制。。。。
        time.sleep(5)

def search(keyword):
    print("Hello!")
    os.system("whoami")
    print("Search for: "+keyword+"\n")
    conn = sqlite3.connect("CVE.db")
    conn.isolation_level = None
    cur = conn.cursor()
    cur.execute('SELECT * FROM CVEinfo WHERE description_En LIKE \'%{}%\' OR description_Zh LIKE \'%{}%\''.format(keyword,keyword))
    res = cur.fetchall()
    conn.close()
    for data in res:
        print("\033[32m[+]\033[0m "+data[1])
        print("\033[32m[+]\033[0m Url : "+data[2])
        print("\033[32m[+]\033[0m Description-En : "+data[3])
        print("\033[32m[+]\033[0m Description-Zh : "+data[4]+"\n")

if __name__ == "__main__":
    parse = OptionParser()
    parse.add_option("-u",dest="update",action='store_true',help='update the CVEs in today.')
    parse.add_option('-s',dest='search',help='search the CVEs which have the key word.')
    (options,args)=parse.parse_args()

    if options.update or options.search:
        if options.update:
            update()
        if options.search:
            search(options.search)
    else:
        parse.print_help()
        print('\nExample:')
        print('[#]-> python3 TodayCVE.py -u')
        print('[#]-> python3 TodayCVE.py -s linux')