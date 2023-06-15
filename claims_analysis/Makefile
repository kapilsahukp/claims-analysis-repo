.PHONY: lint run

lint:
	isort .
	black .
	mypy .
	flake8 . --ignore=E501,W503

run:
	pip install -e ..
	python main.py