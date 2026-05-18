install:
	pip install -r requirements.txt

train:
	python train_onnx.py

format:
	black *.py

lint:
	pylint --disable=R,C app.py train_onnx.py

test:
	pytest test_app.py -v

build:
	docker build -t iris-onnx .

run:
	docker run -p 5000:5000 iris-onnx

push:
	docker tag iris-onnx b0daelbanna/iris-onnx:v1
	docker push b0daelbanna/iris-onnx:v1

all: install train format lint test
