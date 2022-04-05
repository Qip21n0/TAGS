from datetime import datetime as dt
from tags.util import *
from tags import func
import click
import glob
import os


@click.group()
def grp():
	intro = f"Welcome to TAGS system!!! ({dt.now().strftime('%Y/%m/%d %H:%M:%S')})\n"
	print(intro)
	pass


@grp.command()
@click.option(
		'--change',
		'-c',
		is_flag=True,
		help=normalize_doc('Add this option if you want to modify \
			tags_config.json.')
)
def config(change):
	if change:
		change_config()
	else:
		home = os.path.expanduser('~/')
		if home+'tags_config.json' not in glob.glob(home+'*.json'):
			set_config()

		else:
			click.echo("Input OPTION")


@grp.command()
@click.option(
		'--report', 
		'-r', 
		type=str, 
		default=None, 
		help=normalize_doc('The number of the assignment \
			you want to download (ex. T5, E12)')
)
def download(report):
	if report is None:
		click.echo("ERROR: No number of the assignment.")
	else:
		func.download(report)


@grp.command()
def unzip():
	func.unzip()


@grp.command()
@click.option(
		'--ext', 
		'-e', 
		type=str, 
		default='c', 
		help='Type of the file extension.'
)
def compile(ext):
	if ext != 'c' or ext != 'cpp':
		click.echo("ERROR: Designed extension is not 'c' or 'cpp'.")
	else:
		func.compile(ext)


@grp.command()
@click.option(
		'--modified', 
		'-m', 
		is_flag=True, 
		help=normalize_doc('Add this option if you want to modify \
			test.txt or answer.txt.')
)
def test(modified):
	func.test(modified)


@grp.command()
def show(args):
	show_log()