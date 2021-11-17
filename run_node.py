import time
import torch.nn.functional as F
from tqdm import tqdm

from net.comms import *


def train(dataloader, device, model, optimizer):

	#Start training the model normally.
	for inputs, labels in tqdm(dataloader):
		inputs = inputs.to(device)
		labels = labels.to(device)

		preds = model(inputs)
		loss = F.nll_loss(preds, labels)
		loss.backward()
		optimizer.step()

	return True


def main():

	client = make_socket('127.0.0.1', 6001, bind=False)

	connect_socket(client, '127.0.0.1', 6000)

	data = wait_on_data(client)

	train(*data)

if __name__ == '__main__':
	main()