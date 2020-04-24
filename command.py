from connector import Server


def left_eq(origin_str, keyword):
    return origin_str[:len(keyword)] == keyword


class Commander:
    def __init__(self):
        self.nscu = Server()


    def input_mode(self):
        while True:
            print(self.nscu.client_list)
            c = input('>')
            if left_eq(c, 'enter'):
                self.nscu.set_connect(int(c[6:]))
                print('cur_connect: ' + str(self.nscu.current_connect[0]))

            elif left_eq(c, 'cmd'):
                if len(c) > 3:
                    print(self.nscu.send_command(c[4:]))
                else:
                    print(self.nscu.send_command(input('input command: ')))

            elif left_eq(c, 'file_send'):
                c = c.split(' ')
                if len(c) == 2:
                    print('Success') if self.nscu.send_file(c[1]) else print('Fail')
                elif len(c) == 3:
                    print('Success') if self.nscu.send_file(c[1], c[2]) else print('Fail')

            elif left_eq(c, 'file_receive'):
                c = c.split(' ')
                if len(c) == 2:
                    print('Success') if self.nscu.receive_file(c[1]) else print('Fail')
                elif len(c) == 3:
                    print('Success') if self.nscu.receive_file(c[1], c[2]) else print('Fail')
                

if __name__ == '__main__':
    c = Commander()
    c.input_mode()
