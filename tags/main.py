from tags.util import *
from tags.repl import *
from tags.cmds import *
import sys



def main():
	args = sys.argv[1:]
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
	main()