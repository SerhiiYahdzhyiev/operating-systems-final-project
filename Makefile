req_filename := requirements.txt
artifacts := dist/ build/ *.egg-info **/*.egg-info

prepenv:
	python -m venv venv

install:
	pip install -r requirements.txt

freeze:
	pip freeze > $(req_filename)

clean:
	rm -rf $(artifacts)

pinstall:
	pip install -e .

lint:
	ruff check

lfix:
	ruff check --fix

format:
	ruff format
