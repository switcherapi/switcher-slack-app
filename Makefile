.PHONY: build run test cover

install:
	pip install -r requirements.txt

install-test:
	pip install -r tests/requirements.txt

run:
	python src/app.py

test:
	pytest --cov=src

cover:
	coverage html