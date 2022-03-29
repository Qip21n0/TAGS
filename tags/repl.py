from datetime import datetime as dt
from cmd import Cmd
from func import *
from util import *
import readline
import re



class TagsCmd(Cmd):
	intro = re.sub('\t', '', f"""\
		TAGS ({dt.now().strftime('%Y/%m/%d %H:%M:%S')})
		Type \"help\" for more information.
		Press [Ctl + C] or [Ctl + D] to exit this mode.
		======================== \
		""")
	prompt = 'TAGS>> '

	def __init__(self):
		super().__init__()

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


	def do_compile(self, path):
		compile(path)

	def help_compile(self):
		doc = normalize_func_doc(compile)
		print(doc)


	def do_test(self, path):
		test(path)

	def help_test(self):
		doc = normalize_func_doc(test)
		print(doc)


	def do_hoge(self, args):
		for arg in args.split():
			print(arg)

	def help_hoge(self):
		print('help: hoge')