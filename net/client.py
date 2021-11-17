import socket
import ssl
import pickle


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 60000

CLIENT_HOST = "127.0.0.1"
CLIENT_PORT = 60002

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

client = ssl.wrap_socket(client, keyfile="../MyKey.key", certfile="../MyCertificate.crt")

if __name__ == "__main__":
    client.bind((CLIENT_HOST, CLIENT_PORT))
    client.connect((SERVER_HOST, SERVER_PORT))

    while True:
        from time import sleep

        client.send(pickle.dumps("Hello World!"))
        sleep(1)