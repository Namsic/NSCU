import socket, threading


class SocketBinder():
    def __init__(self):
        # Set basic info
        self.ADDR = ('', 3056)
        self.SIZE = 1024
        self.client_list = []
        
        # receive client parallel
        receive_client = threading.Thread(target=self.receive_connect)
        receive_client.daemon = True
        receive_client.start()

        # renew client parallel
        #renew_client = threading.Thread(target=self.renew_client_list)
        #renew_client.daemon = True
        #renew_client.start()
        

    # add client to list when new client is connected 
    def receive_connect(self):
        with socket.socket() as server_socket:
            server_socket.bind(self.ADDR)
            server_socket.listen()
            while True:
                client_socket, client_addr = server_socket.accept()
                name = client_socket.recv(self.SIZE).decode()
                print('\nNew connect: {}\n>>> '.format(name), end='')
                self.client_list.append((name, client_socket))


    # remove client to list when error occurs
    def terminate_connect(self, i):
        print('Disconnected [ {} ]\n>>> '.format(self.client_list[i][0]))
        self.client_list[i][1].close()
        del self.client_list[i]


    # send ' ' to all client for check connection
    def renew_client_list(self):
        for i in range(len(self.client_list)-1, -1, -1):
            self.client_list[i][1].sendall(' '.encode())
            if self.client_list[i][1].recv(self.SIZE).decode() == 'Error':
                self.terminate_connect(i)


    # return client_list
    def get_client_list(self):
        if len(self.client_list)==0:
            print('No client')
            return
        for i in range(len(self.client_list)):
            print('[ {}, {} ]'.format(i, self.client_list[i][0]))


if __name__ == '__main__':
    pass

