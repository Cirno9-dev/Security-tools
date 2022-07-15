# PackAnal

The ip2Loc database uses GeoLite2-City_20200303.tar.gz.<br>
You can get it from <a href='https://www.maxmind.com/'>maxmind</a><br>
You can update the database by yourself.<br>
It can analysis th packet.

# Usage

```shell
cd PackAnal
pip install geoip2 dpkt
python PackAnal.py
```

# Example

```shell
python PackAnal.py -p test.pcapng
```
