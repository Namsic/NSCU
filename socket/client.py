import socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 3056
SIZE = 1024
SERVER_ADDR = (SERVER_IP, SERVER_PORT)

def send_to_server(socket, data):
    socket.send(data.encode())

while True:
    d = input("//")
    if d == "exit":
        break
    with socket.socket() as client_socket:
        client_socket.connect(SERVER_ADDR)
        send_to_server(client_socket, d)
        msg = client_socket.recv(SIZE).decode()
        print("recv : {}".format(msg))
