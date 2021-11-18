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
	
	data = pickle.loads(fernet.decrypt(encrypted))

	func = data["train_function"]
	args = data["args"]
	kwargs = data["kwargs"]
	model_arg_id = data["model_arg_id"]

	ret = func(*args, *kwargs)

	encrypted_return = fernet.encrypt(pickle.dumps(ret))

	with open("encrypted_return.pickle", 'wb') as f:
		pickle.dump(encrypted_return, f)

	with open("encrypted_model.pickle", 'wb') as f:
		pickle.dump(args[model_arg_id], f)

if __name__ == "__main__":
	main()
