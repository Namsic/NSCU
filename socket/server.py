import socket

IP = ''
PORT = 3056
SIZE = 1024
ADDR = (IP, PORT)

with socket.socket() as server_socket:
    server_socket.bind(ADDR)
    server_socket.listen()

    while True:
        client_socket, client_addr = server_socket.accept()
        msg = client_socket.recv(SIZE).decode()
        print("{} : {}".format(client_addr, msg))
        formated_msg = "Server Recieve '{}'".format(msg)
        client_socket.sendall(formated_msg.encode())

        client_socket.close()
