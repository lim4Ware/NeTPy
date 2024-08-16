# NeTPy
NeTPy is a simple TCP connection tool that can be useful in cases of CTF or Pentest in limited scenarios.
![image](https://github.com/user-attachments/assets/a4f3e3a8-283c-47d2-b2d4-6eac7b7c8365)

-- Requirements:
- Python 3.x
- Modules (Default):
  - `argparse`
  - `socket`
  - `shlex`
  - `subprocess`
  - `sys`
  - `textwrap`
  - `threading`

# Instalation: 
`git clone https://github.com/lim4Ware/NeTPy.git`

# Usage:
[SERVER LISTENING - COMMAND SHELL MODE (-c, --command)]
This mode enables the use of command execution (shell) directly on the server that is listening, an alternative to reverse shell.
Just run the command below on the server you want to open a shell on and from any other machine, connect to the IP/Port of this server:
`netpy.py -t 192.168.1.101 -p 5555 -l -c

[SERVER LISTENING - REMOTE COMMAND MODE (-e, --execute)]
This mode enables the preloading of commands on the server that is listening, causing it to send the result of the previously configured command directly to the connection made on the defined IP/Port. Example:
`netpy.py -t 192.168.1.101 -p 5555 -l -e="cat /etc/passwd"
  
