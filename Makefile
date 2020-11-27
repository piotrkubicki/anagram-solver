test:
	pytest tests/

run:
	python main.py

install-dev:
	pip install -e ".[dev]"
