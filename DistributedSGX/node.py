import dill as pickle
import subprocess
from cryptography.fernet import Fernet

from DistributedSGX.networking import *


def init(node_address, node_port, host_address, host_port):

	client = make_socket(node_address, node_port, bind=False)

	connect_socket(client, host_address, host_port)

	return client

def init_crypto():

	key = Fernet.generate_key()

	with open('filekey.key', 'wb') as filekey:
		filekey.write(key)

	return Fernet(key)

def run_node(node_address, node_port, host_address, host_port):

	client = init(node_address, node_port, host_address, host_port)

	fernet = init_crypto()

	encrypted_data = fernet.encrypt(wait_on_data(client))

	with open("args", 'wb') as f:
		pickle.dump(encrypted_data, f)

	#data[0](*data[1:])

def init_manifest():
	subprocess.run(["make"])