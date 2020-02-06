# FtpAttack

```
 /$$$$$$$$ /$$                /$$$$$$    /$$     /$$                         /$$      
| $$_____/| $$               /$$__  $$  | $$    | $$                        | $$      
| $$     /$$$$$$    /$$$$$$ | $$  \ $$ /$$$$$$ /$$$$$$    /$$$$$$   /$$$$$$$| $$   /$$
| $$$$$ |_  $$_/   /$$__  $$| $$$$$$$$|_  $$_/|_  $$_/   |____  $$ /$$_____/| $$  /$$/
| $$__/   | $$    | $$  \ $$| $$__  $$  | $$    | $$      /$$$$$$$| $$      | $$$$$$/ 
| $$      | $$ /$$| $$  | $$| $$  | $$  | $$ /$$| $$ /$$ /$$__  $$| $$      | $$_  $$ 
| $$      |  $$$$/| $$$$$$$/| $$  | $$  |  $$$$/|  $$$$/|  $$$$$$$|  $$$$$$$| $$ \  $$
|__/       \___/  | $$____/ |__/  |__/   \___/   \___/   \_______/ \_______/|__/  \__/
                  | $$                                                                
                  | $$                                                                
                  |__/                                                                

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
A tool to attack the ftp<br>
It is used to test anonymous login and blast FTP account passwords.<br>
In the future, I'll also add the ability to upload trojans and malicious code.<br>
A multithreaded burst will be added shortly<br>

**2020.2.6**<br>
**Add the Vsftpd_234_backdoor vulnerability detection function**

## Usage

```shell
cd FtpAttack
python FtpAttack.py
```

## Example

```shell
python FtpAttack.py -t 127.0.0.1
```
Default port 21

```shell
python FtpAttack.py -t 127.0.0.1 -p 26
```

```shell
python FtpAttack.py -t 127.0.0.1 -f ftp.txt
```
**Ftp.txt is the account password dictionary, each line is: user password**<br>
**You can use your dictionary.**