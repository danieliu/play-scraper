build:
	python setup.py sdist bdist_wheel

clean:
	python setup.py clean --all

lint:
	flake8 play_scraper tests

publish:
	pip install 'twine>=1.5.0'
	twine upload dist/*
	rm -fr build dist .egg play_scraper.egg-info

test:
	python -m unittest discover

test-debug:
	python -m unittest discover -v

.PHONY: build
