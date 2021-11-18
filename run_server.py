import datetime
import os
import argparse

import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import torch.optim as optim
import torch.nn.functional as F
import torch.nn as nn
from tqdm import tqdm

from DistributedSGX.server import distributed_sgx

@distributed_sgx(num_nodes=1)
def train(dataloader, device, model, optimizer):
	#Start training the model normally.
	i = 0
	for inputs, labels in tqdm(dataloader):
		i += 1

		if i == 100:
			break

		inputs = inputs.to(device)
		labels = labels.to(device)

		preds = model(inputs)
		loss = F.nll_loss(preds, labels)
		loss.backward()
		optimizer.step()

	return True

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output

def main():

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


	train(dataloader, device, model, optimizer)


if __name__ == '__main__':
	main()

