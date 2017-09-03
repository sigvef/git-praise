# -*- coding: utf-8 -*-
from __future__ import print_function
from git.exc import InvalidGitRepositoryError
from git.repo.base import Repo
from praise.praise_command import praise
import click
import os


@click.command()
@click.argument('filename')
def praise_command(filename=None):
    try:
        repo = Repo(path=os.getcwd(), search_parent_directories=True)
    except InvalidGitRepositoryError:
        print('Not a git repository')
        return
    try:
        output = praise(filename, repo)
        terminal_height, terminal_width = os.popen(
            'stty size', 'r').read().split()
        lines = output.split('\n')
        if len(lines) > int(terminal_height):
            click.echo_via_pager(output)
        else:
            click.echo(output)
    except Exception:
        print(filename, 'is a binary file.')


if __name__ == '__main__':
    praise_command()
