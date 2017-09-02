.PHONY: all
all:
	pip install -r requirements.txt

.PHONY: setup
setup:
	python -m virtualenv venv -p python3

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	find . -type d -empty -delete
	rm -rf dist git_praise.egg-info

.PHONY: upload-to-pypi
upload-to-pypi:
	python setup.py sdist upload

.PHONY: lint
lint:
	flake8 setup.py praise/**
