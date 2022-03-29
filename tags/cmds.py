from datetime import datetime as dt
from email.policy import default
from util import *
import func
import click


@click.group()
def grp():
	intro = f"TAGS ({dt.now().strftime('%Y/%m/%d %H:%M:%S')})\n"
	print(intro)
	pass

@grp.command()
@click.option('--name', '-n', default='World')
def en(name):
	message = "Hello " + name + "!!!"
	click.echo(message)

@grp.command()
def jp():
	click.echo("KON~~~!!!!!")


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
		'--path', 
		'-p', 
		type=str, 
		default=None, 
		help=''
)
def compile(path):
	if path is None:
		click.echo("ERROR")
	else:
		func.compile(path)


@grp.command()
@click.option(
		'--path', 
		'-p', 
		type=str, 
		default=None, 
		help=''
)
def test(path):
	if path is None:
		click.echo("ERROR")
	else:
		func.test(path)