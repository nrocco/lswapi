PACKAGE ?= lswapi
prefix ?= /usr

install:
	python setup.py install --prefix="$(prefix)" --root="$(DESTDIR)" --optimize=1

clean:
	rm -rf .tox *.egg dist build .coverage
	find $(PACKAGE) -name '__pycache__' -delete -print -o -name '*.pyc' -delete -print

test:
		python setup.py test

publish:
	python setup.py register
	python setup.py sdist upload

.PHONY: install clean test publish
