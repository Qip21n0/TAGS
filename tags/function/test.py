from tags.function.base import BasicTAGS
from tags.util import *
import subprocess
import glob
import re
import os



class TAGSTester(BasicTAGS):
	def __init__(self, tags_path):
		super().__init__(tags_path)
		self.test_path = os.path.join('.', 'test.txt')
		self.answer_path = os.path.join('.', 'answer.txt')

		if not self.exists():
			self.modify()


	def exists(self):
		return os.path.exists(self.test_path) and os.path.exists(self.answer_path)


	def modify(self):
		print("Write some tests & answers.")
		print("(Example) test <= 1 2")
		print("(Example) answer <= 4\n")
		count = 0
		tests = []
		answers = []
		while 1:
			test = input(f'test[{count}] <= ')
			answer = input(f'answer[{count}] <= ')
			print()
			if test == '' or answer == '':
				break
			else:
				tests.append(test)
				answers.append(answer)
				count += 1
		
		with open(self.test_path, 'w') as f:
			f.write('\n'.join(tests))
		with open(self.answer_path, 'w') as f:
			f.write('\n'.join(answers))


	def test(self, exetime=60):
		if not self.exists():
			self.modify()

		tests = []
		with open(self.test_path, 'r') as f:
			lines = f.read()
			for line in lines.split("\n"):
				tests.append(line)
		answers = []
		with open(self.answer_path, 'r') as f:
			lines = f.read()
			for line in lines.split("\n"):
				answers.append(line)

		student_id = self.config_data['student_id']
		is_exefile = lambda filename: filename.isdecimal() and filename.isascii()
		for id in student_id:
			print('=' * 32)
			print("student: " + Color.CYAN +f'{id}'+ Color.END +'\n')
			score = 0

			exefile = 'Not Exists'
			candidates = glob.glob(str(id)+'*')
			for candidate in candidates:
				if is_exefile(candidate):
					exefile = os.path.join('.', candidate)
			if exefile == 'Not Exists':
				print(f'ERROR: No executable file of student {id}')
				continue
			
			for i, test in enumerate(tests):
				if test == '':
					break
				is_correct = True

				try:
					p1 = subprocess.Popen(['echo', test], stdout=subprocess.PIPE)
					p2 = subprocess.Popen([exefile], text=True, stdin=p1.stdout, stdout=subprocess.PIPE)
					p1.stdout.close()
					output, _ = p2.communicate(timeout=exetime)

				except subprocess.TimeoutExpired:
					output = Color.YELLOW + 'TimeOutExpired' + Color.END
					is_correct = False

				except UnicodeDecodeError:
					output = Color.YELLOW + 'UnicodeDecodeError' + Color.END
					is_correct = False

				except Exception as e:
					print(e)
					output = Color.YELLOW + 'Exception' + Color.END
					is_correct = False

				if is_correct:
					print(Color.GREEN+f'ANSWER[{i}]'+Color.END)
					print(answers[i])
					answer = answers[i].split()
					is_correct = self.evaluate(output, answer)

					print(Color.RED+f'TEST[{i}]'+Color.END)
					print(output)
				else:
					print(output)

				if is_correct:
					score += 1

				print()
			print(f'SCORE: {score}/{len(answers)}')


	def evaluate(self, output, answer):
		delimiter = 0
		for ans in answer:
			delimited_output = output[delimiter:]
			MatchObj = re.search(rf'{ans}', delimited_output)
			if MatchObj is None:
				return False
			delimiter = MatchObj.end()

		return True