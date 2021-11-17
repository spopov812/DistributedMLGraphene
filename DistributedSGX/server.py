from DistributedSGX.networking import *


def init(num_nodes):

	if num_nodes < 1:
		raise ValueError("Number of nodes must be greater than 0")

	client = make_socket('127.0.0.1', 6000)
	connections = wait_on_connections(client, num_nodes)

	return connections


def distributed_sgx(num_nodes=-1):

	def decorator(func):

		connections = init(num_nodes)

		def wrapper(*args, **kwargs):

			send_data_all(connections, [func, *args, *kwargs])

			return empty_func

		return wrapper

	return decorator

def empty_func():
	pass