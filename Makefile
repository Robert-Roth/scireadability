.PHONY: dist

install:
	pip install .

test:
	pipenv run pytest test.py

style:
	pipenv run flake8 --max-line-length 88 scireadability/ test.py conftest.py

clean:
	rm -rf build/ dist/ scireadability.egg-info/ __pycache__/ */__pycache__/
	rm -f *.pyc */*.pyc

dist:
	pipenv run python -m build

upload:
	pipenv run twine upload dist/*

