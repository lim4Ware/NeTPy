import argparse     # module for creating command line interfaces
import socket       # module for handling network connections
import shlex        # module for splitting strings into tokens, useful for shell commands
import subprocess   # module for handling operating system processes
import sys          # module for manipulating variables and interactions with the Python interpreter
import textwrap     # module for manipulating and formatting texts
import threading    # module to create and manage threads (parallel executions)

# ascii art for banner
ascii_art = '''
    ╔═╗─╔╗─╔════╦═══╗
    ║║╚╗║║─║╔╗╔╗║╔═╗║
    ║╔╗╚╝╠═╩╣║║╚╣╚═╝╠╗─╔╗
    ║║╚╗║║║═╣║║─║╔══╣║─║║
    ║║─║║║║═╣║║─║║──║╚═╝║
    ╚╝─╚═╩══╝╚╝─╚╝──╚═╗╔╝
    \033[1mPython Net Tool\033[0m─╔═╝║
    \033[1m\033[31m@lim4Ware\033[0m───────╚══╝
    A VERY simple and objective tool
'''
# static help page 
static_help = ''' \033[1m\033[32m[INFO]\033[0m \033[1mUsage\033[0m: netpy.py [-h HELP] [-c COMMAND SHELL] [-e REMOTE COMMAND] 
                    [-l LISTEN MODE] [-t TARGET IP] [-p TARGET PORT]

 \033[1m\033[32m[INFO]\033[0m \033[1mUsage \033[1mcommand \033[1mshell \033[1mexample\033[0m: 
        (\033[1mserver listening\033[0m): netpy.py -t 192.168.1.101 -p 5555 -l -c
        (\033[1mclient mmachine\033[0m): netpy.py -t 192.168.1.101 -p 5555
'''
# show ascii banner
print(ascii_art)

# colors XD
text_alert_info = ' \033[1m\033[32m[INFO]\033[0m ' 
text_alert_error = ' \033[1m\033[31m[ERROR]\033[0m '
text_alert_warning = ' \033[1m\033[32m[WARN]\033[0m '
text_alert_success = ' \033[1m\033[34m[DONE]\033[0m '
text_enable_bold = '\033[1m'
text_disable_bold = '\033[0m'

# function to execute operating system commands
def execute(cmd):
    cmd = cmd.strip()  # remove whitespace at the beginning and end of the 'cmd' string
    if not cmd:        # if the command is empty, the function does nothing and returns
        return
    try:
        # execute system command, and capture output (stdout and stderr)
        output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
        # decodes output from bytes to string and returns
        return output.decode()
    except subprocess.CalledProcessError as e:
        # handles the error if the command fails
        return f"{text_alert_error}Failed executing command: {e.output.decode()}"

# class that implements NetCat logic
class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args      # stores passed arguments
        self.buffer = buffer  # stores the data buffer (can be None or b'')
        # create a socket TCP/IPv4
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # configures the socket to reuse the address, avoiding errors when restarting the server
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # main method that decides whether NetCat will send data or listen
    def run(self):
        # check if it is in listen mode with execute
        if self.args.listen and self.args.execute:
            # sends personalized message about the chosen mode and command
            print(f'{text_alert_info}{text_enable_bold}Listen Mode{text_disable_bold}: Remote Command')
            print(f'{text_alert_success}{text_enable_bold}Command ready to be sent:{text_disable_bold} {self.args.execute}')
            self.listen()

        if self.args.listen and self.args.command:
            print(f'{text_alert_info}{text_enable_bold}Listen Mode{text_disable_bold}: Command Shell')
            print(f'{text_alert_info}{text_enable_bold}Waiting for connection...{text_disable_bold}')
            self.listen()  # if it is in listen mode, call the listen method
        else:
            print(f'{text_alert_info}{text_enable_bold}Active Mode{text_disable_bold}')
            self.send()    # otherwise, call the send method

    # method to send data to the server or receive from the client
    def send(self):
        try:
            # connects to the specified IP address and port
            self.socket.connect((self.args.target, self.args.port))
            print(f'{text_alert_success}{text_enable_bold}Connection Success!{text_disable_bold}')
            print(f'{text_alert_info}{text_enable_bold}Target{text_disable_bold}: {self.args.target}:{self.args.port}')
            if self.buffer:
                # if there is a buffer to send, send the data
                self.socket.send(self.buffer)

            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    # receives data from the socket in 4096 byte chunks
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()  # decode bytes to string
                    if recv_len < 4096:
                        break  # exit the loop if there is no more data to receive
                if response:
                    if " .NeTPy > " in response:
                        command = input(response)
                    else:
                        print(response)
                        command = input('')
                    command += '\n'
                    self.socket.send(command.encode())  # send the encoded buffer
        except KeyboardInterrupt:
            print('Closing...')
            self.socket.close()  # close socket
            sys.exit()  # close script
        except Exception as e:
            print(f"An error occurred: {str(e)}")  # show error
            self.socket.close()  # close socket
            sys.exit()

    # method for listening for connections and processing them
    def listen(self):
        try:
            # associates the socket with the specified IP address and port
            self.socket.bind((self.args.target, self.args.port))
            self.socket.listen(5)  # listening for connections with a backlog of 5

            while True:
                # accept the client connection
                client_socket, address = self.socket.accept()
                print(f'{text_alert_success}{text_enable_bold}New connection received: {text_disable_bold}{address[0]}:{address[1]}')
                # create a new thread to handle the connection with the client
                client_thread = threading.Thread(
                                    target=self.handle, args=(client_socket,)
                )
                client_thread.start()  # start thread
        except Exception as e:
            print(f"An error occurred while trying to listen: {str(e)}")
            self.socket.close()
            sys.exit()

    # method for handling client connection
    def handle(self, client_socket):
        client_address = client_socket.getpeername()
        try:
            if self.args.execute:
                # if the --execute option was used, execute the command and send the output
                print(f'{text_alert_success}{text_enable_bold}Command sent:{text_disable_bold} {self.args.execute}')
                output = execute(self.args.execute)
                client_socket.send(output.encode())
            elif self.args.upload:
                # if the --upload option was used, receive the file and save it locally
                file_buffer = b''
                while True:
                    data = client_socket.recv(4096)
                    if data:
                        file_buffer += data
                    else:
                        break
                with open(self.args.upload, 'wb') as f:
                    f.write(file_buffer)
                message = f'File save as: {self.args.upload}'
                client_socket.send(message.encode())
            elif self.args.command:
                # if the --command option was used, start an interactive shell
                cmd_buffer = b''
                while True:
                    client_socket.send(b' .NeTPy > ') # wait command client
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())

                    command = cmd_buffer.decode().strip()
                    print(f'{text_alert_info}{text_enable_bold}Command Receive{text_disable_bold}: {command}')
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
        except Exception as e:
            print(f"Error handling client: {str(e)}")
            client_socket.close()
            self.socket.close()
            sys.exit()
        finally:
            print(f'{text_alert_info}{text_enable_bold}Connection closed with: {client_address[0]}:{client_address[1]}{text_disable_bold}')
            client_socket.close()

# script entry point
if __name__ == '__main__':
    # create a command line argument parser
    parser = argparse.ArgumentParser(
                formatter_class=argparse.RawDescriptionHelpFormatter,
                epilog=textwrap.dedent('''\
Usage Example: 
netcat.py -t 192.168.1.108 -p 5555 -l -c # Command Shell
''')

    )

    # adds arguments that can be passed via the command line when calling the script
    parser.add_argument('-c','--command', action='store_true', help='Command Shell')
    parser.add_argument('-e', '--execute', help='Remote Command Execute')
    parser.add_argument('-l', '--listen', action='store_true', help='Listening Mode')
    parser.add_argument('-p', '--port', type=int, default=5555, help='Target Port (default: 5555)')
    parser.add_argument('-t', '--target', default='127.0.0.1', help='Target IP (default: localhost)')
    parser.add_argument('-u', '--upload', help='Remote File Upload')


    # checks if any arguments were passed; If not, display help
    if len(sys.argv) == 1:
        print(static_help)
        sys.exit(1)

    # check arguments
    args = parser.parse_args()

    # Start buffer (b'')
    buffer = b''

    # creates and runs an instance of the NetCat class in all cases
    nc = NetCat(args, buffer)
    nc.run()
