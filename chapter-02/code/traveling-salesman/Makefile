install:
	pip install -r requirements.txt

format:
	black *.py

lint:
	pylint --disable=R,C tsp.py

test:
	pytest test_tsp.py -v

run:
	python tsp.py Cairo

all: install format lint test
