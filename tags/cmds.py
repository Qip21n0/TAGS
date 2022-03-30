from datetime import datetime as dt
from email.policy import default
from util import *
import func
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
		is_flag=True
)
def config(change):
	if change:
		change_config()
	else:
		home = os.path.expanduser('~/')
		if home+'tags_config.txt' not in glob.glob(home+'*.txt'):
			set_config()

		else:
			click.echo("Input OPTION")


@grp.command()
@click.option(
		'--url', 
		'-u', 
		type=str, 
		default=None, 
		help=''
)
def download(url):
	if url is None:
		click.echo("ERROR")
	else:
		func.download(url)


@grp.command()
@click.option(
		'--path', 
		'-p', 
		type=str, 
		default=None, 
		help=''
)
def unzip(path):
	if path is None:
		click.echo("ERROR")
	else:
		func.unzip(path)


@grp.command()
@click.option(
		'--ext', 
		'-e', 
		type=str, 
		default='c', 
		help=''
)
def compile(ext):
	if ext is None:
		click.echo("ERROR")
	else:
		func.compile(ext)


@grp.command()
@click.option(
		'--modified', 
		'-m', 
		is_flag=True, 
		help=''
)
def test(modified):
	func.test(modified)