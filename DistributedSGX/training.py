import os
import cloudpickle as pickle
from cryptography.fernet import Fernet


def main():

	with open('filekey.key', 'rb') as filekey:
		key = filekey.read()

	print(key)

	fernet = Fernet(key)

	with open('args.pickle', 'rb') as f:
		encrypted = pickle.load(f)
	
	args = pickle.loads(fernet.decrypt(encrypted))

	args[0](*args[1:])

if __name__ == "__main__":
	main()
