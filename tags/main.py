from tags.mode import cmds
from tags.mode import repl
import sys



def main():
	args = sys.argv[1:]
	if len(args) > 0:
		cmds.grp()

	else:
		try:
			repl.TagsCmd().cmdloop()
		except KeyboardInterrupt:
			print("Keyboard Interrupt [Ctl + C]\n")
			print("GoodBye!!!!")
			pass

if __name__ == '__main__':
	main()