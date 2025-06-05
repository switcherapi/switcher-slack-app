.PHONY: install run test cover

install:
	pipenv install --dev

run:
	python src/app.py

test:
	pytest -v --cov=./src --cov-report xml

cover:
	coverage html