# BannerScan

This is a tool to scan the target's service<br>
Grab the banner of the application to infer the service<br>
It can only be used to scan tcp port.<br>
It does not require additional libraries<br>

# Usage

```shell
cd BannerScan
python BannerScan.py
```

# Example

```shell
python BannerScan.py -t www.example.com -p 80,25,22,21
```

```shell
python BannerScan.py -t 127.0.0.1 -p 80,22,21
```