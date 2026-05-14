install:
	pip install -r requirements.txt

format:
	black *.py

lint:
	pylint --disable=R,C app.py

test:
	pytest test_app.py -v

all: install format lint test
