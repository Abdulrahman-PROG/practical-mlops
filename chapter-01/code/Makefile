install:
	pip install -r requirements.txt

format:
	black *.py

lint:
	pylint --disable=R,C hello.py

test:
	pytest test_hello.py -v

load-test:
	locust -f locustfile.py --headless -u 10 -r 2 --run-time 30s --host http://localhost:8000

all: install format lint test
