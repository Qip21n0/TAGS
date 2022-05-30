from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from tqdm import tqdm
from tags.util import *
import chromedriver_binary
import pyautogui
import subprocess
import glob
import time
import os



def download(report):
	"""
	Download zip files.

	Visit the page corresponding to the given assignment
	and automatically download all zip files with GUI. 

	Parameters
	--------
	r : str
	    ex) T5, E12

	Returns
	--------
	None

	Raises
	--------
	ValueError
	    if url is invalid.
	
	"""
	data = get_config()
	tmp = 'tmp'
	if tmp not in os.listdir(data['dir']):
		os.mkdir(tmp)

	download_path = data['dir'] + SLASH + tmp
	url = data['url'] + '&act_report=1&c=' + data['class'] + '&r=' + report

	options = webdriver.ChromeOptions()
	options.add_argument("--remote-debugging-port=9222") 
	options.add_experimental_option('prefs', {'download.default_directory': download_path})
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	options.use_chromium = True

	browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
	browser.get(url)
	time.sleep(1)

	pyautogui.typewrite(data['id'])
	pyautogui.press('tab')
	pyautogui.typewrite(data['psswd'])
	pyautogui.press('enter')
	time.sleep(2)
	browser.get(url)
	time.sleep(1)

	elements = browser.find_elements_by_xpath("//a[@href]")
	zipfile_url = set()
	for element in elements:
		href = element.get_attribute('href')
		if '&act_download_multi=1'in href:
			zipfile_url.add(href)
		else:
			continue
	
	for i in zipfile_url:
		browser.get(i)
		time.sleep(1)
	
	browser.quit()


def unzip():
	"""
	Unzip zip files.

	Unzip and delete all zip files in `tmp/` directory

	Parameters
	--------
	None

	Returns
	--------
	None

	"""
	data = get_config()
	dir = data['dir'] + SLASH + 'tmp'
	for zip in os.listdir(dir):
		_, ext = os.path.splitext(zip)
		if ext != '.zip':
			os.remove(dir + SLASH + zip)
			continue

		old_name = zip
		new_name = re.findall(r'^([ET][0-9]+_[0-9]+)', zip)[0] + ext
		zip = new_name
		os.rename(dir + SLASH + old_name, dir + SLASH + new_name)

		R = 'R' + re.findall(r'^[ET]([0-9]+)', zip)[0]
		command = 'unzip -q -u ' + dir+SLASH+zip + ' -d ' + data['dir']+SLASH+R
		subprocess.run(command, shell=True)
		os.remove(dir + SLASH + zip)


def compile(ext, option):
	"""
	Compile c or cpp files.

	Compile only the student assignment files whose
	contents have been changed. 

	Parameters
	--------
	ext : str
	    Extension type (ex. c cpp)

	option : list
	    Options to be given at compile time

	Returns
	--------
	None

	Raise
	--------
	ValueError
	    if `ext` is not 'c' or 'cpp', outputs "Invalid
		file extension".

	"""
	student_id = logging(ext)
	opt = " ".join(option)
	if ext == 'cpp' or 'c':
		for id in tqdm(student_id):
			id = str(id)
			file = id + '.' + ext
			compiler = 'gcc' if ext == 'c' else 'g++'

			command = compiler + ' -g -Wall ' + file + ' -o ' + id + ' ' + opt
			subprocess.run(command, shell=True)
		print("COMPILE COMPLETED!!")
		
	else:
		raise ValueError("ERROR: Invalid file extension.")
	

def test(modified):
	"""
	function for test.

	Parameters
	--------
	modified : boolean
	    modify the test items in test.txt when
		`modified` is True.

	Returns
	--------
	None

	"""
	test_path = '.' + SLASH + 'test.txt'
	answer_path = '.' + SLASH + 'answer.txt'

	if test_path not in glob.glob('.'+SLASH+'*.txt') or \
		answer_path not in glob.glob('.'+SLASH+'*.txt') or\
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
	
	print('\033[33m'+'TEST START'+'\033[0m')
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
		print('=' * 32)
		print("student: " + '\033[31m'+f'{id}'+'\033[0m\n')
		score = 0
		id = str(id)
		if '.'+SLASH+id not in glob.glob('.'+SLASH+'*'):
			print(f'ERROR: No executable file of student {id}')
			continue

		for i, t in enumerate(tests):
			if t == '':
				break
			flag = True
			
			try:
				p1 = subprocess.Popen(['echo', t], stdout=subprocess.PIPE)
				p2 = subprocess.Popen(['.'+SLASH+id], stdin=p1.stdout, stdout=subprocess.PIPE)
				p1.stdout.close()
				output = p2.communicate()[0].decode()

			except UnicodeDecodeError:
				output = '\033[33m' + 'UnicodeDecodeError' + '\033[0m'
				flag = False
			except Exception:
				output = '\033[33m' + 'Exception' + '\033[0m'
				flag = False

			if flag:
				print('\033[34m'+f'ANSWER[{i}]'+'\033[0m'+'\t\t'+'\033[32m'+f'TEST[{i}]'+'\033[0m')
				print(answer[i]+'\t\t'+output)
			else:
				print(output)

			answer = answers[i].split()
			for a in answer:
				if a not in output:
					flag = False
			if flag:
				score += 1

			print()
		print(f'SCORE: {score}/{len(answers)}')