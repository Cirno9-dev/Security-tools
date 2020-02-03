import requests
import time
import os
import sys
import threading
from queue import Queue
from optparse import OptionParser
"""
网站目录扫描，字典为directory-list.txt。
字典中一行为一个目录，不需要加后缀，如：index.php只需要index
默认的扫描是['html','htm','txt','js','css']加上特定的后缀，如php/jsp/asp
代码核心是requests中的get()，threading和queue是多线程扫描。
"""
class DirScan():
    def __init__(self,url,suf,th):
        self.url = url
        self.suf = ['html','htm','txt','js','css']
        self.th = th
        if ',' in suf :
            self.suf = suf.split(',')
        elif suf not in self.suf:
            self.suf.append(suf)
        else:
            self.suf = [suf]
        self.judge()

    # 创建多线程扫描，重写run函数
    class thread(threading.Thread):
        def __init__(self,queue,total):
            threading.Thread.__init__(self)
            self.queue = queue
            self.total = total

        def run(self):
            head = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            while not self.queue.empty():
                url = self.queue.get()
                threading.Thread(target=self.progress_bar).start()
                try:
                    # 核心，通过get的状态码来判断，且不允许重定向
                    html = requests.get(url,headers=head,allow_redirects=False)
                    if html.status_code == 200:
                        # 写入到html文件中，方便直接访问
                        f = open(url.split('/')[2]+'.html',"a+")
                        f.write("<a href="+url+">"+url+"</a>")
                        f.write("\n<br>")
                        f.close()
                except Exception as e:
                    print(e)

        # 进度条，方便查看进行到哪里了
        def progress_bar(self):
            sys.stdout.write(' '*20)
            per = 100-float(self.queue.qsize())/float(self.total)*100
            msg = '%s Left [%s All] Scan in %1.1f%%'%(self.queue.qsize(),self.total,per)
            sys.stdout.write('\r'+'[#]'+msg)
            sys.stdout.flush()
            pass

    def start(self):
        queue = Queue()

        # 目录字典
        f = open('directory-list.txt','r')
        # 拼接url放入queue中
        for i in f:
            if '\n' in i:
                i = i.replace('\n','')
            for end in self.suf:
                queue.put(self.url+'/'+i+'.'+end)
        f.close()

        # 给输出文件写入标题
        f = open(self.url.split('/')[2]+'.html',"a+")
        f.write('<h1>'+self.url+'</h1>')
        f.write('\n<br>')
        f.close()

        total = queue.qsize() # url总个数=字典中的数量*后缀数量
        threads = []
        thread_num = self.th # 总线程数

        for i in range(thread_num):
            threads.append(self.thread(queue,total))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    # 判断输入的url是否加上了https://或http://。以及是否存在结果，若存在则结束。
    def judge(self):
        if 'http' not in self.url:
            print('[-] You should add the \'http://\' or \'https://\' in the url')
            exit()
        if os.path.isfile(self.url.split('/')[2]+'.html'):
            print('[-] There are already results: %s'%self.url.split('/')[2]+'.html')
            exit()

if __name__ == "__main__":
    # 输出logo
    print("""
         /$$$$$$$   /$$            /$$$$$$                               
        | $$__  $$|__/           /$$__  $$                              
        | $$  \\ $$ /$$  /$$$$$$ | $$  \\__/  /$$$$$$$  /$$$$$$  /$$$$$$$ 
        | $$  | $$| $$ /$$__  $$|  $$$$$$  /$$_____/ |____  $$| $$__  $$
        | $$  | $$| $$| $$  \\__/ \\____  $$| $$        /$$$$$$$| $$  \\ $$
        | $$  | $$| $$| $$       /$$  \\ $$| $$       /$$__  $$| $$  | $$
        | $$$$$$$/| $$| $$      |  $$$$$$/|  $$$$$$$|  $$$$$$$| $$  | $$
        |_______/ |__/|__/       \\______/  \\_______/ \\_______/|__/  |__/                                                                                                                                             
                                                                        
         /$$                       /$$                                  
        | $$                      | $$                                  
        | $$$$$$$  /$$   /$$      | $$   /$$ /$$   /$$                  
        | $$__  $$| $$  | $$      | $$  |__/|  $$ /$$/                  
        | $$  \\ $$| $$  | $$      | $$   /$$ \\  $$$$/                   
        | $$  | $$| $$  | $$      | $$  | $$  >$$  $$                   
        | $$$$$$$/|  $$$$$$$      | $$  | $$ /$$/\\  $$                  
        |_______/  \\____  $$      |__/  | $$|__/  \\__/                  
                   /$$  | $$       /$$  | $$                            
                  |  $$$$$$/      |  $$$$$$/                            
                   \\______/        \\______/                             
    """)
    # 命令行参数的设定
    oparse = OptionParser()
    oparse.add_option("-u","--url",dest="url",help="url for scanning")
    oparse.add_option("-s","--suf",dest="suf",help="file suffix(php,jsp,asp)")
    oparse.add_option("-t","--thread",dest="th",type="int",default=10,help="scan thread count")
    (options,args) = oparse.parse_args()
    if options.url and options.suf:
        scanner = DirScan(options.url,options.suf,options.th)
        scanner.start()
    else:
        oparse.print_help()
        print("usage example:")
        print("[#]-> python DirScan.py -u http://www.example.com -s php -t 20")
        print("[#]-> html/htm/txt/js/css are all in scanning.If you want scan your want ,please input your option")
        print("[#]-> example: python DirScan.py -u http://www.example.com -s js,php")
        print("[#]-> result file: www.example.com.html")