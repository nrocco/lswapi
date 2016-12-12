#!/usr/bin/env python
import re
import io
import codecs

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class NoseTestCommand(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Run nose ensuring that argv simulates running nosetests directly
        import nose
        nose.run_exit(argv=['nosetests'])


def load_requirements(filename):
    with io.open(filename, encoding='utf-8') as reqfile:
        return [line.strip() for line in reqfile if not line.startswith('#')]


setup(
    name = 'lswapi',
    description = 'a python client library for easy leaseweb api access',
    version = re.search(r'''^__version__\s*=\s*["'](.*)["']''', open('lswapi/__init__.py').read(), re.M).group(1),
    author = 'Nico Di Rocco',
    author_email = 'n.dirocco@global.leaseweb.com',
    url = 'http://developer.leaseweb.com',
    license = 'GPLv3',
    long_description = codecs.open('README.rst', 'rb', 'utf-8').read(),
    test_suite = 'nose.collector',
    download_url = 'https://github.com/nrocco/lswapi/tags',
    include_package_data = True,
    install_requires = load_requirements('requirements.txt'),
    tests_require = [
        'nose',
        'mock',
        'coverage',
    ],
    entry_points = {
        'httpie.plugins.auth.v1': [
            'httpie_lswapi = lswapi.httpie:ApiAuthPlugin'
        ]
    },
    packages = find_packages(),
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    cmdclass = {
        'test': NoseTestCommand
    }
)
