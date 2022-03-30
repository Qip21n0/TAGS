from util import *
from tqdm import tqdm
from zipfile import ZipFile
import subprocess
import difflib
import glob
import sys



def download(url):
	"""
	This is the test.

	Parameters
	--------
	url : str
	    url to get

	Returns
	--------
	str or None
	    Return value

	Raises
	--------
	ValueError
	    if url is invalid.
	"""
	print("OK")


def unzip(path):
	"""
	"""
	with ZipFile(path, 'r') as zip:
		zip.extractall()


def compile(ext):
	"""
	"""
	student_id = get_config()
	if ext == 'cpp' or 'c':
		for id in tqdm(student_id):
			command = 'gcc -g -Wall ' + id + '.' + ext + ' -o ' + id
			subprocess.run(command, shell=True)
		print("COMPILE COMPLETED!!")
		
	else:
		print("ERROR: Invalid file extension.")
		sys.exit(0)
	

def test(modified):
	"""
	"""
	test_path = './test.txt'
	answer_path = './answer.txt'

	if test_path not in glob.glob('./*.txt') or \
		answer_path not in glob.glob('./*.txt') or\
		modified:
		print("Write some tests & answers.")
		print("(Example) \ntest <= 1 2 \nanswer <= 4\n")
		count = 0
		tests = []
		answers = []
		while 1:
			test = input(f'test[{count}] <= ')
			answer = input(f'answer[{count}] <= ')
			if test == '' or answer == '':
				break
			else:
				tests.append(test)
				answers.append(answer)
				count += 1
		
		with open(test_path, 'w') as f:
			f.write('\n'.join(tests))
		with open(answer_path, 'w') as f:
			f.write('\n'.join(answers))

		print()
	
	print('\033[33m'+'TEST START'+'\033[0m\n')
	data = get_config()
	student_id = data['student_id']
	tests = []
	answers = []
	with open(test_path, 'r') as f:
		lines = f.read()
		for line in lines.split("\n"):
			tests.append(line)

	with open(answer_path, 'r') as f:
		lines = f.read()
		for line in lines.split("\n"):
			answers.append(line)

	for id in student_id:
		print("student: " + '\033[31m'+f'{id}'+'\033[0m\n')
		score = len(answers)
		for i, t in enumerate(tests):
			if t == '':
				break
			print('\033[32m'+f'TEST[{i}]'+'\033[0m'+'\t\t'+'\033[34m'+f'ANSWER[{i}]'+'\033[0m')
			print('\t\t'+answers[i], end='')
			command = 'echo ' + t + ' | ' + './' + id + ' | tee diff.txt'
			subprocess.run(command, shell=True)
			
			with open('./diff.txt', 'r') as f:
				out = f.read()
				if answers[i] != out:
					score -= 1

			print()
		print(f'SCORE: {score}/{len(answers)}')
		print('=' * 24)