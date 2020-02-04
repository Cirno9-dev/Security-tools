import socket as s
import time
from optparse import OptionParser

# 实现连接，并发送命令
def connect(target,port):
    CON = (target,port)

    tcpClient = s.socket(s.AF_INET,s.SOCK_STREAM) # 创建socket连接
    tcpClient.connect(CON) # 连接

    print('connecting...')
    data = tcpClient.recv(4096)
    print(data.decode('utf-8'))

    while True:
        raw = input('['+target+']:#')
        # 若输入exit，退出。
        if raw == 'exit':
            break
        tcpClient.send(raw.encode())
        data = tcpClient.recv(4096)
        # 判断返回的信息，若没有这输出并退出
        if not data:
            print('Not receive any data')
            break
        print(data.decode('utf-8'))
    tcpClient.close()

if __name__ == "__main__":
    # 设置命令行参数
    parse = OptionParser()
    parse.add_option('-t','--target',dest='target',help='target host ip')
    parse.add_option('-p','--port',dest='port',type='int',help='target host port')
    (options,args) = parse.parse_args()
    if options.target and options.port:
        connect(options.target,options.port)
    else:
        parse.print_help()
        print('example:')
        print('[#]-> python client.py -t 192.168.1.5 -p 445')