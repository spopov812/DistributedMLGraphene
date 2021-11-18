import socket
import ssl
import pickle

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 60000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server = ssl.wrap_socket(
    server, server_side=True, keyfile="../MyKey.key", certfile="../MyCertificate.crt"
)

if __name__ == "__main__":
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(0)

    while True:
        connection, client_address = server.accept()
        print(connection)
        print(client_address)
        while True:
            data = connection.recv(1024)
            if not data:
                break
            print(f"Received: {pickle.loads(data)}")