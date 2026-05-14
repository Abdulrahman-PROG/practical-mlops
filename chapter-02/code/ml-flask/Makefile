install:
	pip install -r requirements.txt

train:
	python train.py

format:
	black *.py

lint:
	pylint --disable=R,C app.py train.py

test:
	pytest test_app.py -v

all: install train format lint test
