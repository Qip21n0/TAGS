#!/usr/bin/python3

import click


@click.group()
def grp():
	pass


@grp.command()
@click.option('--name', '-n', default='World')
def en(name):
	message = "Hello " + name + "!!!"
	click.echo(message)


@grp.command()
def jp():
	click.echo("KON~~~!!!!!")


def main():
	grp()


if __name__ == '__main__':
	main()