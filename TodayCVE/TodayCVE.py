import requests
import re
from bs4 import BeautifulSoup
import json

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
    return cve_description

def getTranslation(text):
    #调用Google翻译，来对英文描述进行翻译
    url = "https://translate.google.cn/translate_a/single?client=gtx&sl=en&tl=zh-CN&dt=t&q="+text
    jsondata = json.loads(requests.get(url).text)
    translation = ""
    for data in jsondata[0]:
        translation += data[0]
    return translation

if __name__ == "__main__":
    print("\t每天17:02网站更新漏洞.")
    time,cveurls = getCVEurl()
    #输出时间
    print("\t\t"+time[0])
    print("="*50)
    #输出url和编号,描述和中文翻译
    for cveurl in cveurls:
        print("\033[32m[+]\033[0m {} : {}".format("CVE-"+cveurl[1],cveurl[0]))
        description_En = getCVEinfo(cveurl[0])
        print("\033[32m[+]\033[0m Description-En : "+description_En.strip())
        description_Zh = getTranslation(description_En.strip())
        print("\033[32m[+]\033[0m Description-Zh : "+description_Zh.strip()+"\n")