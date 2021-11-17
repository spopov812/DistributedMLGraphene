import argparse
from cryptography.fernet import Fernet


def main():
	with open('filekey.key', 'rb') as filekey:
    	key = filekey.read()

	fernet = Fernet(key)

	with open('args', 'rb') as file:
    	encrypted = file.read()

	args = fernet.decrypt(encrypted)

	args[0](*args[1:])

if __name__ == "__main__":
	main()