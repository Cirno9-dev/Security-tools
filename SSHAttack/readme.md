# SSHAttack

```
  /$$$$$$   /$$$$$$  /$$   /$$  /$$$$$$    /$$     /$$                         /$$      
 /$$__  $$ /$$__  $$| $$  | $$ /$$__  $$  | $$    | $$                        | $$      
| $$  \__/| $$  \__/| $$  | $$| $$  \ $$ /$$$$$$ /$$$$$$    /$$$$$$   /$$$$$$$| $$   /$$
|  $$$$$$ |  $$$$$$ | $$$$$$$$| $$$$$$$$|_  $$_/|_  $$_/   |____  $$ /$$_____/| $$  /$$/
 \____  $$ \____  $$| $$__  $$| $$__  $$  | $$    | $$      /$$$$$$$| $$      | $$$$$$/ 
 /$$  \ $$ /$$  \ $$| $$  | $$| $$  | $$  | $$ /$$| $$ /$$ /$$__  $$| $$      | $$_  $$ 
|  $$$$$$/|  $$$$$$/| $$  | $$| $$  | $$  |  $$$$/|  $$$$/|  $$$$$$$|  $$$$$$$| $$ \  $$
 \______/  \______/ |__/  |__/|__/  |__/   \___/   \___/   \_______/ \_______/|__/  \__/
                   /$$                       /$$                                        
                  | $$                      | $$                                        
                  | $$$$$$$  /$$   /$$      | $$   /$$ /$$   /$$                        
                  | $$__  $$| $$  | $$      | $$  |__/|  $$ /$$/                        
                  | $$  \ $$| $$  | $$      | $$   /$$ \  $$$$/                         
                  | $$  | $$| $$  | $$      | $$  | $$  >$$  $$                         
                  | $$$$$$$/|  $$$$$$$      | $$  | $$ /$$/\  $$                        
                  |_______/  \____  $$      |__/  | $$|__/  \__/                        
                             /$$  | $$       /$$  | $$                                  
                            |  $$$$$$/      |  $$$$$$/                                  
                             \______/        \______/                                   
```
a tool to attack the ssh.<br>
It has two modes.<br>
**MODE 1: SSH Cryptographic Burst Mode.**<br>
**MODE 2: SSH Batch Remote Execution Command Mode.**<br>
In the future, I'll add multithreaded blasting.<br>
**Only for Unix or Linux systems!**

## Usage

```shell
cd SSHAttack
pip install pexpect
python SSHAttack.py
```

## Example

MODE 1: SSH Cryptographic Burst Mode.
```shell
python SSHAttack.py -m 1

[*] Input the target ip,user and password file:192.168.220.140 root passwd ssh.txt
```

MODE 2: SSH Batch Remote Execution Command Mode.
```shell
python SSHAttack.py -m 2

[*] Input the targets file:targets.txt
[*] Input the command:whoami
```