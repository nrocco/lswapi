#!/usr/bin/env python
import io
import codecs

from setuptools import setup, find_packages


def load_requirements(filename):
    with io.open(filename, encoding='utf-8') as reqfile:
        return [line.strip() for line in reqfile if not line.startswith('#')]


setup(
    name='lswapi',
    description='a python client library for easy leaseweb api access',
    version='0.4.2',
    author='Nico Di Rocco',
    author_email='n.dirocco@global.leaseweb.com',
    url='http://developer.leaseweb.com',
    license='GPLv3',
    long_description=codecs.open('README.md', 'rb', 'utf-8').read(),
    download_url='https://github.com/nrocco/lswapi/tags',
    include_package_data=True,
    install_requires=load_requirements('requirements.txt'),
    tests_require=[
        'httpie',
        'coverage',
    ],
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_lswapi = lswapi.httpie:ApiAuthPlugin'
        ]
    },
    packages=find_packages(exclude=['tests']),
    test_suite='tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
)
