import os
import re



def get_tags_path():
	cwd = os.getcwd()
	paths = []
	for path, _, _ in os.walk(HOME):
		if path.endswith('.tags'):
			paths.append(path[:-5])
	
	for path in paths:
		if path in cwd:
			return os.path.join(path, '.tags')

def normalize_doc(doc):
	"""
	Remove the extra tabs.

	Parameters
	--------
	doc : str
	    Text.

	Returns
	--------
	normalized_doc : str
	    Text with tabs removed.

	"""
	return re.sub('\t', '', doc)


HOME = os.path.expanduser('~')
TAGS_PATH = get_tags_path()
CONFIG_PATH = os.path.join(TAGS_PATH, 'config.json')
HISTORY_PATH = os.path.join(TAGS_PATH, 'history.txt')
LAST_DIR_PATH = os.path.join(TAGS_PATH, 'last_dir.txt')