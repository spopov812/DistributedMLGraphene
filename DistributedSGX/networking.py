import socket
import ssl
import cloudpickle as pickle


def make_socket(host, port, bind=True):
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	client = ssl.wrap_socket(client, keyfile="./MyKey.key", certfile="./MyCertificate.crt")

	client.bind((host, port))

	return client


def connect_socket(client, target_host, target_port):

	client.connect((target_host, target_port))

	data = client.recv(1024)

	print(f"Received from server: {pickle.loads(data)}")


def wait_on_connections(client, num_connections):

	client.listen(0)

	connections = []

	while len(connections) < num_connections:
		connection, client_address = client.accept()

		print(f"Connection established with {client_address[0]}:{client_address[1]}")

		connections.append(connection)
		connections[-1].send(pickle.dumps("Server connection established"))

	return connections


def wait_on_data(client):

	chunks = []

	while True:

		chunk = client.recv(2048)

		if chunk == b'':
			break

		chunks.append(chunk)

	return pickle.loads(b''.join(chunks))


def wait_on_data_all(client, num_connections):

	client.listen()

	ret = []

	for _ in range(num_connections):
		_ = client.accept()

		ret.append(wait_on_data(client))

	return ret


def send_data_all(connections, data):

	byte_array = pickle.dumps(data)

	for c in connections:

		c.send(byte_array)
