build:
	python setup.py sdist bdist_wheel

clean:
	python setup.py clean --all

lint:
	flake8 play_scraper tests

publish:
	pip install 'twine>=1.11.0'
	twine upload dist/*
	rm -fr build dist .egg play_scraper.egg-info

publish-test:
	pip install 'twine>=1.11.0'
	twine upload -r test dist/*
	rm -fr build dist .egg play_scraper.egg-info

test:
	python -m unittest discover

test-debug:
	python -m unittest discover -v

.PHONY: build
