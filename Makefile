.PHONY: install install-test run test cover

install:
	pip install -r requirements.txt

install-test:
	pip install -r tests/requirements.txt

run:
	python src/app.py

test:
	pytest -v --cov=./src --cov-report xml

cover:
	coverage html