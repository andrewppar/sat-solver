test: 
	python3 -m unittest  discover -v

check: 
	mypy sat_solver

lint: 
	flake8  sat_solver

doc: 
	cd docs
	make html
