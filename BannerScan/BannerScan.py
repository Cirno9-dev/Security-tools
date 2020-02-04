import socket as s
import threading
from optparse import OptionParser

def conn(host,port):
    global screenLock
    try:
        # tcp连接，并获取banner
        connect = s.socket(s.AF_INET,s.SOCK_STREAM)
        connect.connect((host,port))
        connect.send('BannerScan'.encode())
        result = connect.recv(100)
        screenLock.acquire()
        print('[+] %d/tcp open'%port)
        print('[+] %s\n'%result.decode('utf-8').split(' ')[0])
    except:
        screenLock.acquire()
        print('[-] %d/tcp close\n'%port)
    finally:
        screenLock.release()
        connect.close()

def scan(host,ports):
    try:
        ip = s.gethostbyname(host) # 由网址得到ip/直接得到ip
    except :
        print('[-] Cannot resolve %s:error host!'%host)
        return
    try:
        name = s.gethostbyaddr(ip) # 得到目标计算机的名称
        print('[+] scan result for %s(%s)\n'%(name[0],ip))
    except :
        print('[+] scan result for %s\n'%ip)
    
    for port in ports:
        t = threading.Thread(target=conn,args=(host,int(port)))
        t.start()


if __name__ == "__main__":
    print("""
 /$$$$$$$                                                     /$$$$$$                               
| $$__  $$                                                   /$$__  $$                              
| $$  \\ $$  /$$$$$$  /$$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$ | $$  \\__/  /$$$$$$$  /$$$$$$  /$$$$$$$ 
| $$$$$$$  |____  $$| $$__  $$| $$__  $$ /$$__  $$ /$$__  $$|  $$$$$$  /$$_____/ |____  $$| $$__  $$
| $$__  $$  /$$$$$$$| $$  \\ $$| $$  \\ $$| $$$$$$$$| $$  \\__/ \\____  $$| $$        /$$$$$$$| $$  \\ $$
| $$  \\ $$ /$$__  $$| $$  | $$| $$  | $$| $$_____/| $$       /$$  \\ $$| $$       /$$__  $$| $$  | $$
| $$$$$$$/|  $$$$$$$| $$  | $$| $$  | $$|  $$$$$$$| $$      |  $$$$$$/|  $$$$$$$|  $$$$$$$| $$  | $$
|_______/  \\_______/|__/  |__/|__/  |__/ \\_______/|__/       \\______/  \\_______/ \\_______/|__/  |__/
                                                                                                    
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
    parse.add_option('-t','--tgthost',dest='tgthost',help='target host')
    parse.add_option('-p','--ports',dest='ports',type='string',help='target ports')
    (options,args) = parse.parse_args()
    if options.tgthost and options.ports:
        screenLock = threading.Semaphore(1)
        scan(options.tgthost,options.ports.split(','))
        pass
    else:
        parse.print_help()
        print('example:')
        print('[#]-> python BannerScan.py -t 127.0.0.1 -p 80,25,22,21')
        print('[#]-> python BannerScan.py -t www.example.com -p 80,25')