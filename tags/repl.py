from datetime import datetime as dt
from cmd import Cmd
from tags.func import *
from tags.util import *
import subprocess
import readline
import os



class TagsCmd(Cmd):
	intro = normalize_doc(f"""\
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


	def do_download(self, report):
		reports = report.split()
		for report in reports:
			download(report)

	def help_download(self):
		doc = normalize_doc("""
			Download zip files you want.
			You must enter the number of the assignment 
			you want to download.
			
			Examples
			--------
			TAGS>> download T1
			TAGS>> download E1 E2

			Notes
			--------
			You must have Google Chrome installed
			to this function.
			For Windows users, it is recommended to 
			enable WSLg.
		""")
		print(doc)


	def do_unzip(self, arg):
		unzip()

	def help_unzip(self):
		doc = normalize_doc("""
			Unzip zip files in the tmp/ directory.

			Examples
			--------
			TAGS>> unzip
		""")
		print(doc)


	def do_compile(self, ext):
		if ext == '':
			ext = 'c'
		compile(ext)

	def help_compile(self):
		doc = normalize_doc("""
			Compile c or cpp files.
			If you design the extension, 
			the corresponding compiler will 
			compile the files.

			Examples
			--------
			TAGS>> compile
			TAGS>> compile cpp
		""")
		print(doc)


	def do_test(self, modified):
		modified = True if modified == 'modify' else False
		test(modified)

	def help_test(self):
		doc = normalize_doc("""
			Perform testing with the file describing 
			multiple tests.
			Add `modify` to the end of the command 
			if you want to modify the test file or 
			answer file.

			Examples
			--------
			TAGS>> test
			TAGS>> test modify
		""")
		print(doc)