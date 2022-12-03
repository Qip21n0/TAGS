from tags.function.base import BasicTAGS
from tags.util import Color
import pandas as pd
import subprocess
import datetime
import hashlib
import glob
import os



class TAGSLogger(BasicTAGS):
	def __init__(self):
		super().__init__()
		self.log_path = os.path.join('.', '.log')


	def logging(self):
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
		student_id = self.config_data['student_id']
		path = os.path.join(self.log_path, self.config_data['id']+'.csv')

		if not os.path.exists(self.log_path):
			os.mkdir('.log')

		if path not in os.listdir(self.log_path):
			df = pd.DataFrame(student_id, columns=['id'])
			df.to_csv(path)
			
		df = self.get_log()
		record_num = len(df.columns[1:])
		new_column = []
		add_list = []
		t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

		for id in student_id:
			code = 'Not Submitted'
			candidates = glob.glob(os.path.join('.', str(id)+'.*'))
			for candidate in candidates:
				if os.path.isfile(candidate):
					code = candidate

			if code == 'Not Submitted':
				hash = 0
			else:
				command = ['nkf', '-w', '--overwrite', code]
				subprocess.run(command)
				with open(code, 'r') as f:
					content = f.read()
					hash = hashlib.sha256(content.encode()).hexdigest()
			
				records = df[df['id'].isin([id])].values
				# If not logged, add to the list for addition
				if len(records) == 0:
					records = [0] * record_num
					add_list.append(id)
				else:
					records = records[0][1:]

				# If Compilation run at the same time, a warning is issued and the newer log overwrites the older one.
				if t in df.columns:
					print("Warning!!: Compilation should be run after a period os time.")
					records = records[:-1]

				# Check if the same log already exists.
				print(records)
				if hash in records:
					hash = 1
			
			new_column.append(hash)

		for id in add_list:
			df.loc[id] = 0

		df[t] = new_column
		df.to_csv(path)


	def get_log(self):
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
		csv_path = os.path.join(self.log_path, self.config_data['id']+'.csv')
		return pd.read_csv(csv_path, index_col=0)


	def show_log(self, mode):
		"""
		Show a human-readable from the log.

		Parameters
		--------
		None

		Returns
		--------
		None

		"""
		student_id = self.config_data['student_id']

		if mode == self.config_data['id']:
			df = self.get_log()

		elif os.path.exists(os.path.join(self.log_path, mode+'.csv')):
			df = pd.read_csv(os.path.join(self.log_path, mode+'.csv'), index_col=0)

		elif mode == 'all':
			df = pd.DataFrame(student_id, columns=['id'])
			# Merge CSV files in .log directory
			for file in os.listdir(self.log_path):
				file_path = os.path.join(self.log_path, file)
				add_df = pd.read_csv(file_path, index_col=0)
				df = pd.merge(df, add_df)

			# Put merged log data in chronological order
			df = pd.concat([df.iloc[:, 0], df.iloc[:, 1:].sort_index(axis=1)], axis=1)
			row_num = len(df)
			# Check for duplicate hash values in each row 
			for i in range(row_num):
				records_i = df.iloc[i].values[1:]
				done = set()
				normalized_records = [df.iloc[i, 0]]
				for record in records_i:
					if record in ['0', '1']:
						normalized_records.append(record)
					elif record not in done:
						normalized_records.append(record)
						done.add(record)
					else:
						normalized_records.append("1")
				df.iloc[i] = normalized_records
				
		else:
			print("ERROR: the log file for the ID you specified does not exist.")
			print("IDs you can specify")
			for file in os.listdir(self.log_path):
				file_id = file[:-4]
				print(file_id, end='\t')
			print()
			return None

		print('student id', end='\t')
		for col in df.columns[1:]:
			print(col, end='\t')
		print()
		record_num = len(df.columns[1:])

		for id in student_id:
			# Get records corresponding to id
			records = df[df['id'].isin([id])].values
			if len(records) == 0:
				records = ['0'] * record_num
			else:
				records = records[0][1:]
			print(id, end='\t')

			for record in records:
				record = str(record)

				if record == '0':
					# If not submitted
					output = Color.RED + 'Not submitted' + Color.END
				elif record == '1':
					# If the same as previously submitted
					output = Color.YELLOW + 'Not changed!!' + Color.END
				else:
					# 
					output = Color.GREEN + 'Submitted!!!!' + Color.END

				print(output, end='\t\t')
			print()