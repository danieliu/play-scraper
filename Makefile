build:
	python setup.py sdist bdist_wheel

clean:
	python setup.py clean --all
	rm -rf dist

lint:
	flake8 play_scraper tests

publish: build
	pip install 'twine>=1.11.0'
	twine upload dist/*
	rm -rf build dist .egg play_scraper.egg-info

publish-test: build
	pip install 'twine>=1.11.0'
	twine upload -r test dist/*
	rm -rf build dist .egg play_scraper.egg-info

test:
	python -m unittest discover

test-all:
	detox

test-debug:
	python -m unittest discover -v

.PHONY: build
