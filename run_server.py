import datetime
import os
import argparse

import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import torch.optim as optim

from model import Net
from net.comms import *


def init():

	client = make_socket('127.0.0.1', 6000)
	connections = wait_on_connections(client, 1)

	return connections


def main():

	connections = init()

	#Setup the distributed sampler to split the dataset to each GPU.
	transform=transforms.Compose([
		transforms.ToTensor(),
		transforms.Normalize((0.1307,), (0.3081,))
		])

	dataloader = DataLoader(datasets.MNIST('./data', train=False, download=True, transform=transform))

	#set the cuda device to a GPU allocated to current process .
	device = torch.device('cpu')
	model = Net().to(device)

	optimizer = optim.Adadelta(model.parameters(), lr=0.001)


	send_data_all(connections, [dataloader, device, model, optimizer])


if __name__ == '__main__':
	main()

