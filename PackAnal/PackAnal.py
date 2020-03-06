import dpkt
import socket as s
import geoip2.database
from optparse import OptionParser

# 根据ip得到位置
def getloc(ip):
    reader = geoip2.database.Reader('./database/GeoLite2-City.mmdb')
    try:
        response = reader.city(ip)
        return str(response.subdivisions.most_specific.name)+' , '+str(response.country.name)
    except:
        return 'None'

# 分析数据包并输出写入
def analysis(fileName):
    f1 = open(fileName,'rb')
    if fileName.split('.')[-1] == 'pcapng':
        pacp = dpkt.pcapng.Reader(f1)
    elif fileName.split('.')[-1] == 'pcap':
        pacp = dpkt.pcap.Reader(f1)
    else:
        print('[-] Error pcap/pcapng file')
        exit

    f2 = open('output.txt','wb')
    for (ts,buf) in pacp:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = s.inet_ntop(s.AF_INET,ip.src)
            dst = s.inet_ntop(s.AF_INET,ip.dst)
            print('[*] src:',src,'-> dst:',dst)
            print('[+] src:',getloc(src),'-> dst:',getloc(dst))
            f2.write(('[*] src: '+str(src)+' -> dst: '+str(dst)+'\n').encode())
            f2.write(('[+] src: '+getloc(src)+' -> dst: '+getloc(dst)+'\n\n').encode())
        except:
            continue
    print('\n[*] The output is output.txt')
    f1.close()
    f2.close()

if __name__ == "__main__":
    print('''
 /$$$$$$$                     /$$        /$$$$$$                      /$$
| $$__  $$                   | $$       /$$__  $$                    | $$
| $$  \\ $$ /$$$$$$   /$$$$$$$| $$   /$$| $$  \\ $$ /$$$$$$$   /$$$$$$ | $$
| $$$$$$$/|____  $$ /$$_____/| $$  /$$/| $$$$$$$$| $$__  $$ |____  $$| $$
| $$____/  /$$$$$$$| $$      | $$$$$$/ | $$__  $$| $$  \\ $$  /$$$$$$$| $$
| $$      /$$__  $$| $$      | $$_  $$ | $$  | $$| $$  | $$ /$$__  $$| $$
| $$     |  $$$$$$$|  $$$$$$$| $$ \\  $$| $$  | $$| $$  | $$|  $$$$$$$| $$
|__/      \\_______/ \\_______/|__/  \\__/|__/  |__/|__/  |__/ \\_______/|__/
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
    ''')
    parse = OptionParser()
    parse.add_option('-p','--packet',dest='packet',help='The pcap/pcapng file.')
    (options , args) = parse.parse_args()
    if options.packet:
        analysis(options.packet)
    else:
        parse.print_help()
        print('\nExample:\n')
        print('[#]-> python PackAnal.py -p test.pcapng')