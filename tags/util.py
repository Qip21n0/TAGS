from datetime import datetime
from getpass import getpass
import pandas as pd
import hashlib
import glob
import json
import sys
import re
import os



PATH = os.path.expanduser('~/') + 'tags_config.json'

def normalize_func_doc(func):
	return re.sub('\t', '', func.__doc__)


def set_config():
	print("Start setting for TAGS system.")
	data = {}

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
	with open(PATH, 'r') as f:
		data = json.load(f)
	
	return data


def change_config():
	data = get_config()

	print("url: " + data['url'])
	url = input("If you modify the URL, enter the correct one.")
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
	path = './.log/log.csv'
	with open(path, 'r') as f:
		df = pd.read_csv(f, index_col=0)

	return df


def logging(ext):
	data = get_config()
	student_id = data['student_id']

	path = './.log/log.csv'
	if path not in glob.glob('./.log/*'):
		df = pd.DataFrame(student_id, columns=['id'])
		os.mkdir('.log')
		df.to_csv(path)
		
	df = get_log()
	cwd = glob.glob('./')
	exe_list = []
	new_column = []

	for id in student_id:
		code = './' + str(id) + '.' + ext

		if code not in cwd:
			hash = 0
		else:
			with open(code, 'r') as f:
				content = f.read()
				hash = hashlib.sha256(content.encode()).hexdigest()
		
		if hash not in df[df['id'].isin([id])].values \
			and hash != 0:
			exe_list.append(id)
		else:
			hash = 0
		
		new_column.append(hash)

	t = datetime.today().strftime('%Y-%m-%d')
	df[t] = new_column

	df.to_csv(path)

	return exe_list