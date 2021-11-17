import os
from cryptography.fernet import Fernet


def main():

	print(os.getcwd())

	"""
	with open('filekey.key', 'rb') as filekey:
		key = filekey.read()

	print(key)

	fernet = Fernet(key)

	with open('args.pickle', 'rb') as f:
		encrypted = f.read()
	
	print(type(encrypted))

	args = fernet.decrypt(encrypted)

	"""

	with open('args.pickle', 'rb') as f:
		args = f.read()

	#print(args)

	args[0](*args[1:])

if __name__ == "__main__":
	main()
