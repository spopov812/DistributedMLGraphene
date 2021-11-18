from DistributedSGX.node import run_node
import argparse

parser = argparse.ArgumentParser(description='Distributed ML with SGX node')

parser.add_argument('-np','--node_port', help='Port of this node', required=True, type=int)
parser.add_argument('-sa','--server_address', help='Address of the server', required=True, type=str)
parser.add_argument('-sp','--server_port', help='Port of the server', required=True, type=int)

args = vars(parser.parse_args())

if __name__ == "__main__":

	run_node('127.0.0.1', args['node_port'], args['server_address'], args['server_port'])
