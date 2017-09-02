# git praise
[![Travis](https://img.shields.io/travis/sigvef/git-praise.svg)](https://travis-ci.org/sigvef/git-praise)
[![PyPI](https://img.shields.io/pypi/v/git-praise.svg)](https://pypi.python.org/pypi/git-praise)
[![PyPI](https://img.shields.io/pypi/l/git-praise.svg)](https://pypi.python.org/pypi/git-praise)
[![PyPI](https://img.shields.io/pypi/pyversions/git-praise.svg)](https://pypi.python.org/pypi/git-praise)

A nicer `git blame`.


![Screenshot  of git praise](https://github.com/sigvef/git-praise/blob/master/git-praise.png?raw=true)

## Installation

```
pip install git-praise
```

Make sure that you have your python package bin path in your $PATH.
On Ubuntu, this is `~/.local/bin`.
If it isn't in your path, you can try adding the following to your `.bashrc`:
`export PATH=$PATH:~/.local/bin`.

## Usage

```
$ praise path/to/my/file
```

## Development setup

```
git clone git@github.com:sigvef/git-praise.git
cd git-praise
make setup
. venv/bin/activate
make
```
