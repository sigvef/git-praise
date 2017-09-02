from git.exc import InvalidGitRepositoryError
from git.repo.base import Repo
from praise import praise
from subprocess import PIPE
from subprocess import Popen
import os
import sys

def main():
    try:
        repo = Repo(path=os.getcwd(), search_parent_directories=True)
    except InvalidGitRepositoryError:
        print('Not a git repository')
        return
    filenames = sys.argv[1:2]
    for filename in filenames:
        output = praise(filename, repo)
    terminal_height, terminal_width = os.popen(
        'stty size', 'r').read().split()
    lines = output.split('\n')
    if len(lines) > int(terminal_height):
        with Popen(['less', '-R'], stdin=PIPE) as less:
            less.stdin.write(output.encode('utf8'))
    else:
        print(output)


if __name__ == '__main__':
    main()
