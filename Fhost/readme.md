# Fhost

This is a tool to scan live host.<br>
Because it uses ping ,all may not be accurate.<br>
It uses multiple threads, with a thread count of 15. You can also change the thread_num variable on line 28 to change the number of threads.<br>

## Usage

```shell
cd Fhost
pip install -r requirements.txt
python Fhost.py
```

## Example

```shell
python Fhost.py -i 192.168.1.5
```

```shell
python Fhost.py --ip=192.168.1.0/24
```