# Backdoor

This backdoor is python script, that opens a connection from a victim (reverse shell).

**download_execute.py** - is a python script that doanloads a vitrus to a victim machine.

**listener.py** - is a python script that listens connection from a victim on a selected 
port (ex. 4444) and establishes connection. Afterwards hacker can send commands to a victim.

**win_listener.py** - is a python script that can be converted to a virus through ex. pyinstaller. It can be masquerade to any file (ex. sample.pdf).