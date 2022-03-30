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
		psswd = input("Enter your student password.\n")
		psswd_ = input("Enter your student password again.\n")
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
			psswd = input("Enter new your student password.\n")
			psswd_ = input("Enter new your student password again.\n")
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