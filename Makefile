.PHONY: format lint

format:
	isort .
	black .

lint: format
	flake8 .
