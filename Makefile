.PHONY: install run test cover

install:
	pipenv install --dev

run:
	python src/app.py

gunicorn:
	gunicorn --bind 0.0.0.0:5000 --chdir ./src/ app:slack_app

test:
	pytest -v --cov=./src --cov-report xml

cover:
	coverage html