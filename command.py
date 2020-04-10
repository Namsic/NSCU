from socketbinder import SocketBinder


class Commander:
    def __init__(self, socketbinder):
        self.sb = socketbinder
        self.index = -1
        self._socket = None
        self.SIZE = 1024


    def set_target(self, i):
        if i < 0 or i >= len(self.sb.client_list):
            self.index = -1
            self._socket = None
        else:
            self.index = i
            self._socket = self.sb.client_list[i][1]
            print(self.sb.client_list[i][0])


    def transfer(self, typ):
        self._socket.sendall(typ.encode())
        check = self._socket.recv(self.SIZE).decode()
        if check != 'Ready':
            return check

        elif typ == 'command':
            param = input('input command: ')
            self._socket.sendall(param.encode())
            return self._socket.recv(self.SIZE).decode()

        elif typ == 'file send':
            param = input('my filename: ')
            with open(param, 'rb') as f:
                print('start send...')
                while True:
                    _buff = f.read(self.SIZE)
                    if not _buff:
                        self._socket.sendall(b'99')
                        break
                    self._socket.sendall(_buff)
                    self._socket.recv(self.SIZE)
                        




if __name__ == '__main__':
    sb = SocketBinder()
    c = Commander(sb)

    while True:
        print('command / file send / ... ')
        cmd = input('>>> ')
        cmd = cmd.split(' ')

        if cmd[0] == 'exit':
            break

        elif cmd[0] == 'stat':
            print('now index: {}'.format(c.index))
            c.sb.get_client_list()

        elif cmd[0] == 'enter':
            c.set_target(int(cmd[1]))

        elif c._socket != None:
            print(c.transfer(' '.join(cmd)))
            
