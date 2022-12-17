from datetime import datetime as dt
from tags.function import *
from tags.util import *
from cmd import Cmd
import subprocess
import readline
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
		self.tags_path = get_tags_path()
		if self.tags_path is None:
			print("Create a new TAGS config file because it does not exist.")
			set_config()
		self.basic_tags = BasicTAGS(self.tags_path)


	def do_EOF(self, arg):
		return True


	def emptyline(self):
		return None


	def do_cd(self, line):
		try:
			os.chdir(line)
			with open(self.basic_tags.last_dir_path, mode='w') as f:
				cwd = os.getcwd()
				f.write(cwd)
		except FileNotFoundError:
			print("ERROR: no directories you want to move to.")

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
		
		for i in range(len(completions)):
			p = os.path.join(path, completions[i])
			if os.path.isdir(p):
				completions[i] += '/'

		return completions


	def do_ls(self, arg):
		ls = 'ls -al' if os.name == 'posix' else 'dir'
		subprocess.run(ls, shell=True)


	def do_pwd(self, arg):
		print(os.getcwd())

	
	def do_cat(self, line):
		try:
			subprocess.run("pygmentize -O style=emacs -f console256 -g "+line, shell=True)
			print()
		except:
			print("ERROR: no files you want to see.")
	
	def complete_cat(self, text, line, begidx, endidx):
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

		return completions


	def do_exe(self, line):
		student_id = self.basic_tags.config_data['student_id']
		try:
			exe_file = int(line)
		except:
			print("ERROR: invalid input.")
			return None

		if exe_file not in student_id:
			print("ERROR: No executable file exists for the student number entered.")
		else:
			exe_path = os.path.join('.', line)
			try:
				subprocess.run(exe_path, shell=True)
				print()
			except KeyboardInterrupt:
				print()

	def help_exe(self):
		doc = normalize_doc("""
			Runs the specified executable file.
			
			Examples
			--------
			TAGS>> exe 19870425
		""")
		print(doc)

	def complete_exe(self, text, line, begidx, endidx):
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
		exe_or_dir_list = []
		for file in cwd:
			isascnum = lambda s: True if s.isdecimal() and s.isascii() else False
			if isascnum(file):
				exe_or_dir_list.append(file)

		if filename == '':
			completions = exe_or_dir_list
		else:
			completions = [f for f in exe_or_dir_list if f.startswith(filename)]

		return completions


	def do_download(self, report_num):
		mode = 'all'
		student_number = '12345678'
		while 1:
			print("Which files you want to download?")
			print("- All students [1]")
			print("- Specific student [2]")
			print("- Cancel [3]")
			n = input("Enter only one of the number above => ")
			
			if n == '1':
				mode = 'all'
				break
			elif n == '2':
				mode = 'indiv'
				student_number = input("Enter the student number you want to download => ")
				try:
					student_number = int(student_number)
				except Exception:
					student_number = -1
				if student_number not in self.basic_tags.config_data['student_id']:
					print("Not valid student number.")
				else:
					break
			elif n == '3':
				return
			else:
				print("Valid numbers are 1, 2, or 3.")

		report_nums = report_num.split()
		d = TAGSDownloader(self.tags_path)
		d.download(report_nums, student_number, mode)

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


	def do_compile(self, arg):
		arg_list = arg.split()

		if 'cpp' in arg_list:
			extension = 'cpp'
		else:
			extension = 'c'

		if extension in arg_list:
			arg_list.remove(extension)
		
		options = ' '.join(arg_list)
		c = TAGSCompiler(self.tags_path, extension, options)
		c.compile()

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


	def do_test(self, *arg):
		t = TAGSTester(self.tags_path)
		if len(arg) == 1:
			if arg[0] == '':
				t.test()
			elif arg[0] == 'modify':
				t.modify()
			elif arg[0].isdecimal():
				exetime = int(arg[0])
				t.test(exetime)
			else:
				print("Not valid options.")
			
		else:
			print("too many options.")

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
			TAGS>> test 100
			TAGS>> test modify
		""")
		print(doc)


	def do_show(self, mode):
		if mode == '':
			mode = 'all'
		l = TAGSLogger(self.tags_path)
		l.show_log(mode)
	
	def help_show(self):
		doc = normalize_doc("""
			Visualize contents of log file.
			If you want to see a specific log, 
			please do the corresponding ID

			Examples
			--------
			TAGS>> show
			TAGS>> show abc12345
		""")
		print(doc)