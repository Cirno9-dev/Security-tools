from IPy import IP
import os
import threading
from queue import Queue
from optparse import OptionParser

# 创建多线程
class scan_thread(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            ip = self.queue.get()
            # 使用ping来判断主机是否存活
            result = os.popen('ping '+ip+' -n 1')
            if 'TTL' in str(result.readlines()):
                print('[+]'+ip+' up')

def scan(ips):
    queue = Queue()

    for ip in ips:
        queue.put(str(ip))

    threads = []
    thread_num = 15 # 线程数

    for _ in range(thread_num):
        threads.append(scan_thread(queue))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    # 输出logo
    print("""
     /$$$$$$$$ /$$                             /$$    
    | $$_____/| $$                            | $$    
    | $$      | $$$$$$$   /$$$$$$   /$$$$$$$ /$$$$$$  
    | $$$$$   | $$__  $$ /$$__  $$ /$$_____/|_  $$_/  
    | $$__/   | $$  \\ $$| $$  \\ $$|  $$$$$$   | $$    
    | $$      | $$  | $$| $$  | $$ \\____  $$  | $$ /$$
    | $$      | $$  | $$|  $$$$$$/ /$$$$$$$/  |  $$$$/
    |__/      |__/  |__/ \\______/ |_______/    \\___/  
                                                    
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
    parse.add_option('-i','--ip',dest='ip',help="IP segment to scan")
    (options,args) = parse.parse_args()
    if options.ip:
        ips = IP(options.ip)
        scan(ips)
    else:
        parse.print_help()
        print('\nExample:')
        print('[#]-> python Fhost.py -i 192.168.1.0/24')
        print('[#]-> python Fhost.py -i 192.168.1.5')