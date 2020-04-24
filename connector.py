import socket, threading, time
import nsconfig as ncf
from transfer import Send, Receive

"""
000: Check connection
001: Generate 1:1 connection
002: Terminate 1:1 connection
011: Send command
012: Send File
013: Receive File
"""

# ------------------------------------------------ #
# -------------------* Server *------------------- #
# ------------------------------------------------ #
class Server:
    def __init__(self):
        # [0: socket, 1: IP Addr]
        self.client_list = []
        # for 1:1 commmunication
        # [0: index of client_list, 1: socket]
        self.current_connect = (-1, None)

        # Receive client parallel
        recv_connect = threading.Thread(target=self.receive_connect)
        recv_connect.daemon = True
        recv_connect.start()


    # Receive new client
    def receive_connect(self):
        # Open socket
        with socket.socket() as s:
            s.bind(('', ncf.PORT[0]))
            s.listen()
            while True:
                # Occurred new connection
                _socket, _addr = s.accept()
                self.client_list.append([_socket, _addr])


    # Terminate connect
    def terminate_connect(self, i):
        self.client_list[i][0].close()
        del self.client_list[i]


    # Make 1:1 connection
    def set_connect(self, i):
        # Clean up existing connection
        if self.current_connect[1] != None:
            self.current_connect[0].sendall('002'.encode())
            self.current_connect[1].close()
        
        if i < 0 or i >= len(self.client_list):
            self.current_connect = (-1, None)
            return self.current_connect
        
        _s = socket.socket()
        _s.bind((self.client_list[i][1][0], ncf.PORT[1]))
        _s.listen()
        self.client_list[i][0].sendall('001'.encode())
        self.current_connect = (i, _s.accept()[0])
        return self.current_connect


    def send_command(self, command):
        if self.current_connect[1] == None:
            return
        self.client_list[self.current_connect[0]][0].sendall('011'.encode())
        return Send(self.current_connect[1]).command(command)


    def send_file(self, path, saveas=''):
        if self.current_connect[1] == None:
            return

        # Init saveAs
        if saveas == '':
            saveas = path.replace('/', '\\').split('\\')[-1]
        
        self.client_list[self.current_connect[0]][0].sendall('012'.encode())
        return Send(self.current_connect[1]).file(path, saveas)


    def receive_file(self, path, saveas=''):
        if self.current_connect[1] == None:
            return
        
        # Init saveAs
        if saveas == '':
            saveas = path.replace('/', '\\').split('\\')[-1]

        self.client_list[self.current_connect[0]][0].sendall('013'.encode())
        param = path + '|*|' + saveas
        self.client_list[self.current_connect[0]][0].sendall(param.encode())
        return Receive(self.current_connect[1]).file()


# ------------------------------------------------ #
# -------------------* Client *------------------- #
# ------------------------------------------------ #
class Client:
    def __init__(self):
        self._socket = socket.socket()
        self.try_connect()
        self.connect = None
        self.receive_mode()


    def __del__(self):
        if self.connect != None:
            self.connect.close()
        self._socket.close()


    # Try to connect infinitely 
    def try_connect(self):
        while True:
            try:
                self._socket.connect((ncf.IP, ncf.PORT[0]))
                break
            except ConnectionRefusedError:
                continue


    def receive_mode(self):
        while True:
            recv = self._socket.recv(ncf.SIZE).decode()
            print(recv)
            if recv == '001':
                self.connect = socket.socket()
                self.connect.connect((ncf.IP, ncf.PORT[1]))
                
            elif recv == '002':
                self.connect.close()
                self.cunnect = None

            elif recv == '011':
                if self.connect == None:
                    return
                Receive(self.connect).command()

            elif recv == '012':
                if self.connect == None:
                    return
                Receive(self.connect).file()

            elif recv == '013':
                if self.connect == None:
                    return
                path, saveas = self._socket.recv(ncf.SIZE).decode().split('|*|')
                Send(self.connect).file(path, saveas)
