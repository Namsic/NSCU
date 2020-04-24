from connector import Client


if __name__ == '__main__':
    while True:
        try:
            c = Client()
        except ConnectionResetError:
            continue
