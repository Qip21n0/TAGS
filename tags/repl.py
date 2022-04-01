from datetime import datetime as dt
from cmd import Cmd
from func import *
from util import *
import subprocess
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
		if home+'tags_config.json' not in glob.glob(home+'*.json'):
			set_config()

	def do_EOF(self, arg):
		return True

	def emptyline(self):
		return None

	def do_cd(self, dir):
		if dir == '':
			print("ERROR: no directory you want to move to.")
		else:
			os.chdir(dir)

	def do_ls(self, arg):
		subprocess.run('ls -al', shell=True)


	def do_download(self, r):
		download(r)

	def help_download(self):
		doc = normalize_func_doc(download)
		print(doc)


	def do_unzip(self, arg):
		unzip()

	def help_unzip(self):
		doc = normalize_func_doc(unzip)
		print(doc)


	def do_compile(self, ext):
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