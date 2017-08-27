import sys
from praise import praise

def main():
    filenames = sys.argv[1:]
    for filename in filenames:
        praise(filename)

if __name__ == '__main__':
    main()
