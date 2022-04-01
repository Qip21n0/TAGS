from tags.util import *
from tqdm import tqdm
import subprocess
import shutil
import glob
import sys
import os



def download(r):
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
	data = get_config()
	tmp = 'tmp'
	if tmp not in os.listdir(data['dir']):
		os.mkdir(tmp)

	download_path = data['dir'] + '/' + tmp
	url = data['url'] + '&act_report=1&c=' + data['class'] + '&r=' + r

	print("OK")


def unzip():
	"""
	"""
	data = get_config()
	dir = data['dir'] + '/tmp'
	for zip in os.listdir(dir):
		if '.zip' not in zip:
			continue

		R = 'R' + re.findall(r'^[ET]([0-9]+)', zip)[0]
		shutil.unpack_archive(dir+'/'+zip, data['dir']+'/'+R)
		os.remove(dir+'/'+zip)


def compile(ext):
	"""
	"""
	student_id = logging(ext)
	if ext == 'cpp' or 'c':
		for id in tqdm(student_id):
			id = str(id)
			#command = ['gcc', '-g', '-Wall', id+'.'+ext, '-o', id]
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
			id = str(id)
			#command = ['echo', t, '|', './'+id, '|', 'tee', 'diff.txt']
			command = 'echo ' + t + ' | ' + './' + id + ' | tee diff.txt'
			subprocess.run(command, shell=True)
			
			with open('./diff.txt', 'r') as f:
				out = f.read()
				if answers[i] != out:
					score -= 1

			print()
		print(f'SCORE: {score}/{len(answers)}')
		print('=' * 24)
		
	os.remove('./diff.txt')