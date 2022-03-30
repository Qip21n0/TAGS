import sys
import re
import os



PATH = os.path.expanduser('~/') + 'tags_config.txt'

def normalize_func_doc(func):
	return re.sub('\t', '', func.__doc__)


def set_config():
	print("Start setting for TAGS system.")

	print("Enter a list of all the student numbers for the classes you are responsible for as TA.")
	print("This form stops when a blank character is entered.")
	student_id = []
	while 1:
		num = input()
		if num == '':
			break
		else:
			student_id.append(num)

	with open(PATH, 'w') as f:
		f.write('\n'.join(student_id))
	


def get_config():
	student_id = []
	with open(PATH, 'r') as f:
		lines = f.read()
		for line in lines.split("\n"):
			if line != '':
				student_id.append(line)
	
	return student_id
	


def change_config():
	student_id = get_config()
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

	with open(PATH, 'w') as f:
		f.write('\n'.join(student_id))