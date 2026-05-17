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

build:
	docker build -t iris-classifier .

run:
	docker run -p 5000:5000 iris-classifier

all: install train format lint test
