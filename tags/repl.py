from datetime import datetime as dt
from cmd import Cmd
from unittest import result
from tags.func import *
from tags.util import *
import subprocess
import readline
import glob
import os



class TagsCmd(Cmd):
	intro = normalize_doc(f"""\
		Welcome to TAGS system!!! ({dt.now().strftime('%Y/%m/%d %H:%M:%S')})
		Type \"help\" for more information.
		Press [Ctl + C] or [Ctl + D] to exit this mode.
		================================================ \
		""")
	prompt = 'TAGS>> '

	def __init__(self):
		super().__init__()
		home = os.path.expanduser('~'+SLASH)
		if home+'tags_config.json' not in glob.glob(home+'*.json'):
			set_config()

	def do_EOF(self, arg):
		return True

	def emptyline(self):
		return None


	def do_cd(self, line):
		try:
			os.chdir(line)
		except FileNotFoundError:
			print("ERROR: no directory you want to move to.")

	def complete_cd(self, text, line, begidx, endidx):
		line = line.split()

		if len(line) < 2:
			filename = ''
			path = './'

		else:
			path = line[1]
			if '/' in path:
				i = path.rfind('/')
				filename = path[i+1:]
				path = path[:i]
			else:
				filename = path
				path = './'

		cwd = os.listdir(path)
		if filename == '':
			completions = cwd
		else:
			completions = [f for f in cwd if f.startswith(filename)]

		result = []
		for f in completions:
			if os.path.isdir(f):
				f = '\033[36m' + f + '\033[0m'
			result.append(f)
		return result


	def do_ls(self, arg):
		ls = 'ls -al' if os.name == 'posix' else 'dir'
		subprocess.run(ls, shell=True)


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


	def do_compile(self, arg):
		arg_list = arg.split()

		if 'cpp' in arg_list:
			ext = 'cpp'
		else:
			ext = 'c'

		if ext in arg_list:
			arg_list.remove(ext)
		
		option = arg_list.copy()
		flag = True
		for opt in option:
			if '-' != opt[0]:
				flag = False

		if flag:
			compile(ext, option)
		else:
			print("ERROR: invalid option.")

	def help_compile(self):
		doc = normalize_doc("""
			Compile c or cpp files.
			If you design the extension, 
			the corresponding compiler will 
			compile the files.
			You can add options when compiling.

			Examples
			--------
			TAGS>> compile
			TAGS>> compile c -lm
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


	def do_show(self, args):
		show_log()
	
	def help_show(self):
		doc = normalize_doc("""
			Visualize contents of log file.

			Examples
			--------
			TAGS>> show
		""")
		print(doc)