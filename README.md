
# NETPY - A VERY SIMPLE PYTHON TOOL

NeTPy is a simple TCP connection tool that can be useful in cases of CTF or Pentest in limited scenarios.



## HELP COMMANDS

![image](https://github.com/user-attachments/assets/a4f3e3a8-283c-47d2-b2d4-6eac7b7c8365)


## MODES

- -c, --command
- -e, --execute
- -l, --listen



## REQUIREMENTS
- Python 3.x
- Modules (Default):
  - `argparse`
  - `socket`
  - `shlex`
  - `subprocess`
  - `sys`
  - `textwrap`
  - `threading`
## INSTALATION

Very easy... just git clone:

```bash
  git clone https://github.com/lim4Ware/NeTPy.git
```
    
## USAGE: SERVER LISTENING - COMMAND SHELL MODE
This mode enables the use of command execution (shell) directly on the server that is listening, an alternative to reverse shell.

Just run the command below on the server you want to open a shell on and from any other machine, connect to the IP/Port of this server:

```sh
netpy.py -t 192.168.1.101 -p 5555 -l -c
```
View of server listening:
![image](https://github.com/user-attachments/assets/690b1336-d00c-4408-af0d-99453c115896)

View of client machine: 
![image](https://github.com/user-attachments/assets/09aecd3f-8f50-4070-a5c6-c054e5541342)


## USAGE: SERVER LISTENING - REMOTE COMMAND MODE
This mode enables the preloading of commands on the server that is listening, causing it to send the result of the previously configured command directly to the connection made on the defined IP/Port. Example:

```sh
netpy.py -t 192.168.1.101 -p 5555 -l -e="cat /etc/passwd
```
## WORK TO BE DONE

There's still a lot to improve in this script, I'm trying to implement new features while learning python for offensive security. If you have any suggestions, I'm happy to hear from you :)

