from datetime import datetime
from getpass import getpass
import pandas as pd
import subprocess
import hashlib
import glob
import json
import sys
import re
import os


SLASH = '/' if os.name == 'posix' else '\\'
PATH = os.path.expanduser('~') + SLASH + 'tags_config.json'
LOG_PATH = SLASH.join(['.', '.log', ''])


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


def set_config():
	"""
	Configure settings.

	Configue the necessary settings to run TAGS.
	The following is the contents of `tags_config.json`
	after configuration
	    data = {
			"dir": str,
			"class": str,
			"url": str,
			"id": str,
			"psswd": str,
			"student_id": [
				int,
				int,
				.
				.
				int
			]
		}

	Parameters
	--------
	None

	Returns
	--------
	None

	"""
	print("Start setting for TAGS system.")
	data = {}
	data['dir'] = os.getcwd()
	cls = input('Enter the class you are responsible for\n')
	data['class'] = cls

	url = input("Enter the url of the class submission page.\n")
	data['url'] = url
	print()

	while 1:
		id = input("Enter your student id. (ex. abc123456)\n")
		id_ = input("Enter your student id again.\n")
		print()
		if id == id_:
			break
	while 1:
		psswd = getpass("Enter your student password.\n")
		psswd_ = getpass("Enter your student password again.\n")
		print()
		if psswd == psswd_:
			break
	data['id'] = id
	data['psswd'] = psswd


	print("Enter a list of all the student numbers for the classes you are responsible for as TA.")
	print("This form stops when a blank character is entered.")
	student_id = []
	while 1:
		num = input()
		if num == '':
			break
		else:
			student_id.append(int(num))
	data['student_id'] = student_id

	with open(PATH, 'w') as f:
		json.dump(data, f, indent=4)


def get_config():
	"""
	Get information from the config file.

	Parameters
	--------
	None

	Returns
	--------
	data : dict
	    information in the config file.

	"""
	with open(PATH, 'r') as f:
		data = json.load(f)
	
	return data


def change_config():
	"""
	Change information in the config file.

	Parameters
	--------
	None

	Returns
	--------
	None

	"""
	data = get_config()

	print("url: " + data['url'])
	url = input("If you modify the URL, enter the correct one.\n")
	data['url'] = url


	print("Your ID: " + data['id'])
	print("Your Password: " + data['psswd'])
	flag = input("Could you change your ID or password? [y/n]\n")
	while flag not in ['y', 'n']:
		flag = input('Enter y or n\n')
	if flag == 'y':
		while 1:
			id = input("Enter new your student id. (ex. abc123456)\n")
			id_ = input("Enter new your student id again.\n")
			print()
			if id == id_:
				break
		while 1:
			psswd = getpass("Enter new your student password.\n")
			psswd_ = getpass("Enter new your student password again.\n")
			print()
			if psswd == psswd_:
				break
		data['id'] = id
		data['psswd'] = psswd

	student_id = data['student_id']
	for i, v in enumerate(student_id):
		print(f'[{i}]: {v}')
	
	print("Enter the index you want to change and the student number.")
	print("This form stops when a blank character is entered.")
	while 1:
		i = input('[index] <= ')
		num = input('student number <= ')
		if i == '' or num == '':
			break
		else:
			i = int(i)
			n = len(student_id)
			if i < n:
				student_id[i] = num
			elif i == n:
				student_id.append(num)
			else:
				print("ERROR: The index you entered is not correct.")
				sys.exit(0)
	data['student_id'] = student_id

	with open(PATH, 'w') as f:
		json.dump(data, f, indent=4)


def get_log():
	"""
	Get logs from the log file.

	Parameters
	--------
	None

	Returns
	--------
	df : pandas.DataFrame
	    DataFrame with conveerted the csv file for log

	"""
	data = get_config()
	path = LOG_PATH + data['id'] + '.csv'
	return pd.read_csv(path, index_col=0)


def logging(ext):
	"""
	Log files.

	Read changes from the hash values of the assignment
	files and log them.

	Parameters
	--------
	ext : str
	    Type of the file extension to be logged

	Returns
	--------
	exe_list : list
	    List of files to be compiled

	"""
	data = get_config()
	student_id = data['student_id']
	path = LOG_PATH + data['id'] + '.csv'

	if path not in glob.glob(SLASH.join(['.','.log', '*'])):
		df = pd.DataFrame(student_id, columns=['id'])
		os.mkdir('.log') 
		df.to_csv(path)
		
	df = get_log()
	cwd = glob.glob('./*')
	exe_list = []
	new_column = []
	t = datetime.today().strftime('%Y-%m-%d')

	for id in student_id:
		code = '.' + SLASH + str(id) + '.' + ext

		if code not in cwd:
			hash = 0
		else:
			subprocess.run("nkf -w "+code+' '+ code, shell=True)
			with open(code, 'r') as f:
				content = f.read()
				hash = hashlib.sha256(content.encode()).hexdigest()
		
			record = df[df['id'].isin([id])].values[0][1:]
			if t in df.columns:
				record = record[:-2]

			if hash not in record:
				exe_list.append(id)
			else:
				hash = 1
		
		new_column.append(hash)
	df[t] = new_column

	df.to_csv(path)

	return exe_list


def show_log():
	"""
	Show a human-readable from the log.

	Parameters
	--------
	None

	Returns
	--------
	None

	"""
	data = get_config()
	student_id = data['student_id']
	df = get_log()
	print('id', end='\t\t')

	for col in df.columns[1:]:
		print(col, end='\t')
	print()

	for id in student_id:
		records = df[df['id'].isin([id])].values[0][1:]
		print(id, end='\t')

		for record in records:
			record = str(record)

			if record == '0':
				output = '\033[31m' + 'Not submitted' + '\033[0m'
			elif record == '1':
				output = '\033[33m' + 'Not changed' + '\033[0m'
			else:
				output = '\033[32m' + 'Submitted!!' + '\033[0m'

			print(output, end='\t')
		print()