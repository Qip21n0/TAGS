import os
import json



class BasicTAGS:
	def __init__(self, tags_path):
		config_path = os.path.join(tags_path, 'config.json')
		with open(config_path, 'r') as f:
			self.config_data = json.load(f)
		self.history_path = os.path.join(tags_path, 'history.txt')
		self.last_dir_path = os.path.join(tags_path, 'last_dir.txt')

	"""
	def _get_tags_path(self):
		home_path = os.path.expanduser('~')
		cwd = os.getcwd()
		paths = []
		for path, _, _ in os.walk(home_path):
			if path.endswith('.tags'):
				paths.append(path[:-6])
	
		for path in paths:
			if path in cwd:
				return os.path.join(path, '.tags')
	"""