import re



def normalize_func_doc(func):
	return re.sub('\t', '', func.__doc__)


def set_config():
	pass


def get_config():
	pass


def change_config():
	pass