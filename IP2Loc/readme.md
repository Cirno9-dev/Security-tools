# IP2Loc

A tool to get some information from the IP.<br>
The database is from <a href='https://www.maxmind.com/'>maxmind</a>.<br>
Database uses GeoLite2-City_20200616.tar.gz.<br>
You can update the database by yourself.<br>

# Usage

```shell
cd IP2Loc
pip install geoip2
python IP2Loc.py
```

# Example

```shell
python IP2Loc.py -p 128.101.101.101
```