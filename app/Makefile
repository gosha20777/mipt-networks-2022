deps:
	pip install --upgrade pip pip-tools
	pip-compile requirements.in
	pip-compile dev-requirements.in

	pip-sync requirements.txt dev-requirements.txt  

lint:
	isort .
	flake8 .

test:
	pytest -vv