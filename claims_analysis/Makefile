.PHONY: lint

lint:
	isort .
	black .
	mypy .
	flake8 . --ignore=E501,W503