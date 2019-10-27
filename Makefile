.PHONY: test
test:
	pip install httpie
	python setup.py test


.PHONY: clear
clear:
	find lswapi tests -name '*.pyc' -exec rm -f {} +
	find lswapi tests -name '*.pyo' -exec rm -f {} +
	find lswapi tests -name '*~' -exec rm -f {} +
	find lswapi tests -name '._*' -exec rm -f {} +
	find lswapi tests -name '.coverage*' -exec rm -f {} +
	rm -rf .tox *.egg dist build .coverage MANIFEST || true
