from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from getpass import getpass
import chromedriver_binary
import urllib
import json
import os
import re



class Color:
    BLACK     = '\033[30m'
    RED       = '\033[31m'
    GREEN     = '\033[32m'
    YELLOW    = '\033[33m'
    BLUE      = '\033[34m'
    PURPLE    = '\033[35m'
    CYAN      = '\033[36m'
    WHITE     = '\033[37m'
    END       = '\033[0m'



def set_config():
	"""
	Configure settings.

	Configue the necessary settings to run TAGS.
	The following is the contents of `config.json`
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
	config_data = {}
	cwd = os.getcwd()
	config_data['dir'] = cwd

	class_num = input("Enter the "+Color.GREEN+"class "+Color.END+"you are responsible for => ")
	config_data['class'] = class_num

	url = input("Enter the "+Color.GREEN+"URL "+Color.END+"of the class submission page.\n")
	config_data['url'] = url
	print()

	while 1:
		id = input("Enter your "+Color.GREEN+"student ID"+Color.END+". (ex. abc123456) => ")
		id_ = input("Enter your "+Color.GREEN+"student ID "+Color.END+"again. => ")
		print()
		if id == id_:
			break
		else:
			print("No match. Enter again.")
	while 1:
		passwd = getpass("Enter your student "+Color.GREEN+"password"+Color.END+". => ")
		passwd_ = getpass("Enter your student "+Color.GREEN+"password "+Color.END+"again. => ")
		print()
		if passwd == passwd_:
			break
		else:
			print("No match. Enter again.")
	config_data['id'] =  urllib.parse.quote(id)
	config_data['passwd'] =  urllib.parse.quote(passwd)


	# Check the url os valid.
	protocol = url.find("://") + 3
	authorized_url = url[:protocol] + id + ':' + passwd + '@' + url[protocol:]
	authorized_url1 = authorized_url + '&act_report=1&c=' + class_num

	options = webdriver.ChromeOptions()
	options.add_argument('--headless')
	options.add_argument("--remote-debugging-port=9222") 
	options.use_chromium = True
	browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

	browser.get(authorized_url1)
	title = browser.title
	if title == '401 Unauthorized' or title == '404 Not Found':
		raise Exception("cannot reach the class submission page. Set your config "+Color.RED+"again."+Color.END)
	
	else:
		authorized_url2 = authorized_url + '&act_report=1&c=' + class_num
		browser.get(authorized_url2)
		elements = browser.find_elements_by_tag_name('td:nth-child(1)')
		student_id = []
		for element in elements:
			if re.fullmatch(r'\d{8}', element.text) is not None:
				student_id.append(int(element.text))
		
		print(Color.CYAN+"Student number"+Color.END)
		for id in student_id:
			print(id)

		config_data['student_id'] = student_id

		if '.tags' not in os.listdir(cwd):
			os.mkdir('.tags')
		config_path = os.path.join(cwd, '.tags', 'config.json')
		with open(config_path, 'w') as f:
			json.dump(config_data, f, indent=4)



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