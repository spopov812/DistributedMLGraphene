import cloudpickle as pickle
import subprocess
from cryptography.fernet import Fernet
import os

from DistributedSGX.networking import *


def init(node_address, node_port, host_address, host_port):

	client = make_socket(node_address, node_port)
	connect_socket(client, host_address, host_port)

	return client

def init_crypto():

	key = Fernet.generate_key()

	with open('./DistributedSGX/filekey.key', 'wb') as filekey:
		filekey.write(key)

	return Fernet(key)

def run_node(node_address, node_port, host_address, host_port):

	client = init(node_address, node_port, host_address, host_port)
	fernet = init_crypto()
	data = wait_on_data(client)

	encrypted_data = fernet.encrypt(pickle.dumps(data))

	with open("./DistributedSGX/args.pickle", 'wb') as f:
		pickle.dump(encrypted_data, f)

	graphene()

def graphene():
	print("Starting graphene")
	os.chdir("./DistributedSGX")
	subprocess.run(["make"])
	subprocess.run(["graphene-direct", "pytorch", "training.py"])
	os.chdir("..")
