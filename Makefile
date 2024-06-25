req_filename := requirements.txt
artifacts := ./build/ ./dist/ ./*.egg-info ./**/*.egg-info

freeze:
	pip freeze > $(req_filename)

clean:
	rmdir $(artifacts) /s /q

dev-pkg-install:
	pip install -e .

