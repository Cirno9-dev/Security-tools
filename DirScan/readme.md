# DirScan

This is a directory scan tool.<br>
The dictionary is directory-list.txt. <br>
The directory, do not need to add suffixes, such as: index.php only need index.<br>
Default scan is ['html','htm','txt','js','css'] add specific suffix, such as PHP/JSP/asp. <br>
The core of the code is get() in requests, and threading and queue are multithreaded scans. <br>
The result file is www.example.com.html.  The output is an HTML file for easy access to the url<br>

## Usage

```shell
cd DirScan
python DirScan.py
```

## Example

```shell
python DirScan.py -u https://www.baidu.com -s php -t 20
```
It will scan js, HTML, CSS, HTM, and PHP files.

```shell
python DirScan.py -u https://www.baidu.com -s js,html,php
```
It will scan js, HTML, and PHP files.

```shell
python DirScan.py -u https://www.baidu.com -s js
```
It will scan js files.