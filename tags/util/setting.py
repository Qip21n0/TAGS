from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from tags.util.setting import get_config
from tags.util.util import CONFIG_PATH
from getpass import getpass
import chromedriver_binary
import urllib
import json
import sys
import os
import re



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
	with open(CONFIG_PATH, 'r') as f:
		data = json.load(f)
	
	return data


class TAGSConfig:
	def __init__(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--headless')
		options.add_argument("--remote-debugging-port=9222") 
		options.use_chromium = True
		self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

	def set_config(self):
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
		self.data = {}
		self.data['dir'] = os.getcwd()

		cls = input('Enter the \033[32mclass\033[0m you are responsible for => ')
		self.data['class'] = cls

		url = input("Enter the \033[32mURL\033[0m of the class submission page.\n")
		self.data['url'] = url
		print()

		while 1:
			id = input("Enter your \033[32mstudent ID\033[0m. (ex. abc123456) => ")
			id_ = input("Enter your \033[32mstudent ID\033[0m again. => ")
			print()
			if id == id_:
				break
		while 1:
			passwd = getpass("Enter your student \033[32mpassword\033[0m. => ")
			passwd_ = getpass("Enter your student \033[32mpassword\033[0m again. => ")
			print()
			if passwd == passwd_:
				break
		self.data['id'] =  urllib.parse.quote(id)
		self.data['passwd'] =  urllib.parse.quote(passwd)

		if self._check_url():
			self._get_student_id()

			with open(CONFIG_PATH, 'w') as f:
				json.dump(self.data, f, indent=4)

		else:
			print("ERROR: cannot reach the class submission page. Set your config \033[31magain\033[0m.")
			self.set_config()

	def _authorized(self, url):
		protocol = url.find('://') + 3
		return url[:protocol] + self.data['id'] + ":" + self.data['passwd'] + '@' + url[protocol:]

	def _check_url(self):
		url = self.data['url'] + '&act_report=1&c=' + self.data['class']
		url = self._authorized(url)
		self.browser.get(url)

		if self.browser.title == '401 Unauthorized':
			return False
		else:
			return True

	def _get_student_id(self):
		url = self.data['url'] + '&act_report=1&c=' + self.data['class']
		url = self._authorized(url)
		self.browser.get(url)

		elements = self.browser.find_elements_by_tag_name('td:nth-child(1)')
		student_id = []
		for element in elements:
			if re.fullmatch(r'\d{8}', element.text) is not None:
				student_id.append(int(element.text))

		self.data['student_id'] = student_id


	def change_config(self):
		"""
		Change information in the config file.

		Parameters
		--------
		None

		Returns
		--------
		None

		"""
		self.data = get_config()

		print("Current class: " + self.data['class'])
		cls = input('If you modify the \033[32mclass\033[0m, enter the correct one. => ')
		if cls != '':
			self.data['class'] = cls

		print("Current url: " + self.data['url'])
		url = input("If you modify the \033[32mURL\033[0m, enter the correct one. =>")
		if url != '':
			self.data['url'] = url

		print("Your ID: " + self.data['id'])
		print("Your Password: " + self.data['passwd'])
		flag = input("Could you change your \033[32mID\033[0m or \033[32mpassword\033[0m? [y/n] => ")
		while flag not in ['y', 'n']:
			flag = input('Enter y or n\n')
		if flag == 'y':
			while 1:
				id = input("Enter new your \033[32mstudent ID\033[0m. (ex. abc123456) => ")
				id_ = input("Enter new your \033[32mstudent ID\033[0m again. => ")
				print()
				if id == id_:
					break
			while 1:
				passwd = getpass("Enter new your \033[32mstudent password\033[0m. => ")
				passwd_ = getpass("Enter new your \033[32mstudent password\033[0m again. => ")
				print()
				if passwd == passwd_:
					break
			self.data['id'] =  urllib.parse.quote(id)
			self.data['passwd'] =  urllib.parse.quote(passwd)

		if self._check_url():
			self._get_student_id()

			with open(CONFIG_PATH, 'w') as f:
				json.dump(self.data, f, indent=4)

		else:
			print("ERROR: cannot reach the class submission page. Set your config \033[31magain\033[0m.")
			self.change_config()