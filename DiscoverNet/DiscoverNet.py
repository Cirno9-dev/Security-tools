import winreg
import time
from requests import get

def val2addr(val):
    addr = ""
    try:
        for ch in val:
            addr += ("%02x "% ch)
        addr = addr.strip(" ").replace(" ",":")[0:17]
        return addr
    except :
        return None

def printNets():
    net = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\NetworkList\\Signatures\\Unmanaged"
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, net)
    print('\n[*] Networks You have Joined.')
    for i in range(100):
        try:
            guid = winreg.EnumKey(key, i)
            netKey = winreg.OpenKey(key, str(guid))
            (n, addr, t) = winreg.EnumValue(netKey, 5)
            (n, name, t) = winreg.EnumValue(netKey, 4)
            macAddr = val2addr(addr)
            netName = str(name)
            if macAddr != None:
                GPS = getGPS(macAddr)
            else:
                GPS = None
            print('[+] '+netName+' '*(40-len(netName.encode('gbk')))+str(macAddr)+' '*(22-len(str(macAddr)))+str(GPS))
            winreg.CloseKey(netKey)
        except:
            break

def getGPS(macAddr):
    loctime = time.localtime(time.time())
    urltime = ""
    for t in loctime:
        t = str(t)
        if len(t) == 1:
            t = '0'+t
        urltime += t
    urltime = urltime[:14]
    url = "https://api.wigle.net/api/v2/network/search?netid=%s&ssid=&latrange1=&latrange2=&longrange1=&longrange2=&lastupdt=%s"%(macAddr,urltime)
    cookie = {"auth":"ljx542233302%3A921282316%3A1581473592%3A0loYKlKxUwYlceA4XEXD2w"}
    jsondata = get(url,cookies=cookie).json()
    if jsondata['success']:
        if jsondata['totalResults'] == 0:
            return None
        else:
            return jsondata['results'][0]
    else:
        return False

if __name__ == "__main__":
    printNets()
    getGPS("3c:a5:81:78:d9:ed")