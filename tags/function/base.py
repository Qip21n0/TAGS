import os
import json



class BasicTAGS:
	def __init__(self):
		self.home_path = os.path.expanduser('~')
		self.tags_path = self._get_tags_path()
		self.config_path = os.path.join(self.tags_path, 'config.json')
		self.history_path = os.path.join(self.tags_path, 'history.txt')
		self.last_dir_path = os.path.join(self.tags_path, 'last_dir.txt')

	
	def _get_tags_path(self):
		cwd = os.getcwd()
		paths = []
		for path, _, _ in os.walk(self.home_path):
			if path.endswith('.tags'):
				paths.append(path[:-6])
	
		for path in paths:
			if path in cwd:
				return os.path.join(path, '.tags')


	def load(self, filename):
		if filename == 'config':
			with open(self.config_path, 'r') as f:
				self.config_data = json.load(f)

		elif filename == 'history':
			with open(self.history_path, 'r') as f:
				self.history = f.readlines()

		elif filename == 'last_dir':
			with open(self.last_dir_path, 'r') as f:
				self.last_dir = f.readlines()[-1]

		else:
			raise NameError("Not valid file name.")