from tags.function.base import BasicTAGS
from tags.function.logging import TAGSLogger
from tqdm import tqdm
import subprocess



class TAGSCompiler(BasicTAGS):
	def __init__(self, extension, options):
		super().__init__()
		self.load('config')
		self.extension = extension
		self.options = options
		self.compiler = self._set_compiler()


	def _set_compiler(self):
		if self.extension == 'c':
			return 'gcc'
		elif self.extension == 'cpp':
			return 'g++'
		else:
			raise ValueError("ERROR: Invalid file extension.")


	def compile(self):
		l = TAGSLogger()
		l.logging()
		
		student_id = self.config_data['student_id']
		for id in tqdm(student_id):
			str_id = str(id)
			file = str_id + '.' + self.extension
			command = " ".join([self.compiler, '-g', '-Wall', file, '-o', str_id, self.options])
			subprocess.run(command, shell=True)

		print("COMPILE COMPLETED!!")