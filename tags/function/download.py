from tags.function.base import BasicTAGS
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from tqdm import tqdm
import chromedriver_binary
import subprocess
import html
import time
import re
import os



class TAGSDownloader(BasicTAGS):
	def __init__(self):
		super().__init__()
		self.load('config')
		self.download_path = self._set_download_path()
		self.browser = self._set_browser()


	def _set_download_path(self):
		download_dirname = 'tmp'
		if download_dirname not in os.listdir(self.config_data['dir']):
			os.mkdir(download_dirname)
		return os.path.join(self.config_data['dir'], download_dirname)


	def _set_browser(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--headless')
		options.add_argument("--remote-debugging-port=9222") 
		options.add_experimental_option('prefs', {'download.default_directory': self.download_path})
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		options.use_chromium = True
		return webdriver.Chrome(ChromeDriverManager().install(), options=options)


	def _authorized(self, url):
		protocol = url.find('://') + 3
		return url[:protocol] + self.config_data['id'] + ":" + self.config_data['passwd'] + '@' + url[protocol:]


	def download(self, report_num, student_id, mode):
		if mode == '' or mode == 'all':
			self.download_all(report_num)
		elif mode == 'indiv' and student_id in self.config_data['student_id']:
			self.download_indiv(report_num, student_id)
		else:
			raise ValueError("Not Valid Mode. Select [all(default), indiv]")


	def download_all(self, reports):
		for report in tqdm(reports):
			url = self.config_data['url'] + '&act_report=1&c=' + self.config_data['class'] + '&r=' + report
			url = self._authorized(url)
			self.browser.get(url)

			elements = self.browser.find_elements_by_xpath("//a[@href]")
			zipfile_url = set()
			for element in elements:
				href = element.get_attribute('href')
				if '&act_download_multi=1'in href:
					zipfile_url.add(href)
				else:
					continue

			for i in zipfile_url:
				self.browser.get(i)
				time.sleep(1)
			
			report_num =  'R' + re.findall(r'([0-9]+)', report)[0]
			self.unzip(report_num)
		self.browser.quit()


	def download_indiv(self, report_num, student_id):
		for report in tqdm(report_num):
			try:
				report_initial = report.split('_')[0]
				extension = report.split('.')[1]
				url = self.data['url'] + '&act_item=1&s=' + student_id + '&r=' + report_initial + '&i=' + report
				url = self._authorized(url)
				self.browser.get(url)
				student_code = html.unescape(self.browser.page_source[131:-20])
				
				code_path = os.path.join(self.config_data['dir'], report_initial, report, student_id+'.'+extension)
				with open(code_path, mode='w') as f:
					f.write(student_code)

			except Exception as e:
				print(e)
				continue

	
	def unzip(self, report_num=None):
		if report_num is None:
			print("Specify the correct report number")
			return

		for zipfile in os.listdir(self.download_path):
			old_zipfilename, extension = os.path.splitext(zipfile)
			if extension != '.zip':
				remove_filepath = os.path.join(self.download_path, zipfile)
				os.remove(remove_filepath)
				continue

			zipfile_path = os.path.join(self.download_path, zipfile)
			destination_dir = os.path.join(self.config_data['dir'], report_num)
			new_dirname = re.finall(r'(.*)-', old_zipfilename)[0]
			destination = os.path.join(destination_dir, new_dirname)

			command = ['unzip', '-qq', '-o', '-j', zipfile_path, '-d', destination]
			subprocess.run(command)

			os.remove(zipfile_path)