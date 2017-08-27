.PHONY: all
all:
	pip install -r requirements.txt

.PHONY: setup
setup:
	python -m virtualenv venv -p python3
