from datetime import datetime as dt
from cmd import Cmd
from func import *
from util import *
import readline
import re
import os



class TagsCmd(Cmd):
	intro = re.sub('\t', '', f"""\
		Welcome to TAGS system!!! ({dt.now().strftime('%Y/%m/%d %H:%M:%S')})
		Type \"help\" for more information.
		Press [Ctl + C] or [Ctl + D] to exit this mode.
		======================== \
		""")
	prompt = 'TAGS>> '

	def __init__(self):
		super().__init__()
		home = os.path.expanduser('~/')
		if home+'tags_config.txt' not in glob.glob(home+'*.txt'):
			set_config()

	def do_EOF(self, arg):
		return True

	def emptyline(self):
		return None


	def do_download(self, url):
		download(url)

	def help_download(self):
		doc = normalize_func_doc(download)
		print(doc)


	def do_unzip(self, path):
		unzip(path)

	def help_unzip(self):
		doc = normalize_func_doc(unzip)
		print(doc)


	def do_compile(self, ext='c'):
		if ext == '':
			ext = 'c'
		compile(ext)

	def help_compile(self):
		doc = normalize_func_doc(compile)
		print(doc)


	def do_test(self, modified):
		modified = True if modified == 'mdfy' else False
		test(modified)

	def help_test(self):
		doc = normalize_func_doc(test)
		print(doc)