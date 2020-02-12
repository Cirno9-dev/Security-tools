import geoip2.database
from optparse import OptionParser

# 根据ip得到位置
def getLoc(ip):
    reader = geoip2.database.Reader('./database/GeoLite2-City.mmdb')
    response = reader.city(ip)
    print('\n[*] Result for %s\n'%ip)
    if response.country.name == None:
        print('[+] country:\t\t',response.country.name)
    else:
        print('[+] country:\t\t',response.country.name,response.country.names['zh-CN'])
    if response.subdivisions.most_specific.name == None:
        print('[+] region:\t\t',response.subdivisions.most_specific.name)
    else:
        print('[+] region:\t\t',response.subdivisions.most_specific.name,response.subdivisions.most_specific.names['zh-CN'])
    if response.city.name == None:
        print('[+] city:\t\t',response.city.name)
    else:
        print('[+] city:\t\t',response.city.name,response.city.names['zh-CN'])
    print('[+] postal code:\t',response.postal.code)
    print('[+] latitude:\t\t',response.location.latitude)
    print('[+] longtitude:\t\t',response.location.longitude)
    print('[+] network:\t\t',response.traits.network)
    reader.close()

if __name__ == "__main__":
    print("""
     /$$$$$$ /$$$$$$$   /$$$$$$  /$$                          
    |_  $$_/| $$__  $$ /$$__  $$| $$                          
      | $$  | $$  \\ $$|__/  \\ $$| $$        /$$$$$$   /$$$$$$$
      | $$  | $$$$$$$/  /$$$$$$/| $$       /$$__  $$ /$$_____/
      | $$  | $$____/  /$$____/ | $$      | $$  \\ $$| $$      
      | $$  | $$      | $$      | $$      | $$  | $$| $$      
     /$$$$$$| $$      | $$$$$$$$| $$$$$$$$|  $$$$$$/|  $$$$$$$
    |______/|__/      |________/|________/ \\______/  \\_______/
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
    parse = OptionParser()
    parse.add_option('-p','--ip',dest='ip',help='The ip you want get postion')
    (options , args) = parse.parse_args()
    if options.ip:
        getLoc(options.ip)
        pass
    else:
        parse.print_help()
        print('\nExample:')
        print('[#]-> python IP2Loc.py -p 8.8.8.8')