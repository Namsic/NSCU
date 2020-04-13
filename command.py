from socketbinder import SocketBinder
import os


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


    def receive(self, size=0):
        if size == 0:
            size = self.SIZE
        recv = self._socket.recv(size)
        if recv.decode()[:5] == 'Error':
            self.sb.terminate_connect(self.index)
            self.set_target(-1)
        return recv


    def transfer(self, typ):
        self._socket.sendall(typ.encode())
        check = self.receive().decode()
        if check != 'Ready':
            return check

        elif typ == 'command':
            param = input('input command: ')
            self._socket.sendall(param.encode())
            return self.receive().decode()

        elif typ == 'file send':
            param1 = input('myfile name: ')
            param2 = input('savefile name: ')
            if param2 == '':
                param2 = param1
            if not os.path.isfile(param1):
                self._socket.sendall('sorry'.encode())
                return '{} not exist'.format(param1)

            self._socket.sendall(param2.encode())
            with open(param1, 'rb') as f:
                while True:
                    _buff = f.read(self.SIZE)
                    if not _buff:
                        self._socket.sendall(b'99')
                        return 'Success'
                    self._socket.sendall(_buff)
                    self.receive()

        elif typ == 'file receive':
            param1 = input('targetfile name: ')
            param2 = input('savefile name: ')
            if param2 == '':
                param2 = param1
            self._socket.sendall(param1.encode())
            if self.receive().decode() == 'sorry':
                return '{} not exist'.format(param1)
            self._socket.sendall('Ready'.encode())
            with open(param2, 'wb') as f:
                while True:
                    _buff = self._socket.receive()
                    if _buff == b'99':
                        return 'Success'
                    else:
                        f.write(_buff)
                        self._socket.sendall('ok'.encode())


        elif typ == 'set alias':
            param = input("{}'s new alias: ".format(self.sb.client_list[self.index][0]))
            self._socket.sendall(param.encode())
            print(self.sb.client_list[self.index][0])
            print(param)




if __name__ == '__main__':
    sb = SocketBinder()
    c = Commander(sb)

    while True:
        if c.index != -1:
            print('\ncommand / file send(receive) / set alias / ... ')
            print('{} / {}'.format(c.index, c.sb.client_list[c.index][0]))
        cmd = input('>>> ')
        if cmd == '':
            continue
        cmd = cmd.split(' ')

        if cmd[0] == 'exit':
            break

        elif cmd[0] == 'stat':
            c.set_target(-1)
            print('now index: {}'.format(c.index))
            c.sb.get_client_list()

        elif cmd[0] == 'enter':
            c.set_target(int(cmd[1]))

        elif c._socket != None:
            print(c.transfer(' '.join(cmd)))
            
