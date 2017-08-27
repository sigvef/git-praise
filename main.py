from git.exc import InvalidGitRepositoryError
from git.repo.base import Repo
from praise import praise
import os
import sys

def main():
    try:
        repo = Repo(path=os.getcwd(), search_parent_directories=True)
    except InvalidGitRepositoryError:
        print('Not a git repository')
        return
    filenames = sys.argv[1:]
    for filename in filenames:
        praise(filename, repo)

if __name__ == '__main__':
    main()
