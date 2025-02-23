ci: clean lint coverage


.PHONY: clean
clean:
	find src tests -name '__pycache__' -exec rm -rf {} +
	find src tests -name '*.pyc' -exec rm -f {} +
	find src tests -name '*.pyo' -exec rm -f {} +
	find src tests -name '*~' -exec rm -f {} +
	find src tests -name '._*' -exec rm -f {} +
	find src tests -name '.coverage*' -exec rm -f {} +
	rm -rf .tox .pytest_cache *.egg *.egg-info dist build htmlcov .coverage MANIFEST


.PHONY: version
version:
	git describe --tags --always | sed -r -e 's/-([0-9]+)/.dev\1/' -e 's/-/+/' | tee .version


.PHONY: lint
lint:
	python3 -m flake8 src tests


.PHONY: test
test:
	python3 -m pytest -vv


.PHONY: coverage
coverage:
	python3 -m pytest -vv --no-cov-on-fail --cov=src --cov-report=term --cov-report=html --cov-report=xml


.PHONY: build
build: clean
	python3 -m build


# The default make target is ci
.DEFAULT_GOAL := ci
