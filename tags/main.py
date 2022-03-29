from util import *
from repl import *
from cmds import *
import sys



def main(args):
	if len(args) > 0:
		grp()

	else:
		try:
			TagsCmd().cmdloop()
		except KeyboardInterrupt:
			print("Keyboard Interrupt [Ctl + C]\n")
			print("GoodBye!!!!")
			pass

if __name__ == '__main__':
	main(sys.argv[1:])