# -*- coding: utf-8 -*-
import re
from setuptools import setup, find_packages

setup(
    name='lswapi',
    version = re.search(r'''^__version__\s*=\s*["'](.*)["']''', open('lswapi/__init__.py').read(), re.M).group(1),
    description='a python client library for easy leaseweb api access',
    long_description = open('README.md').read(),
    author='Nico Di Rocco',
    author_email='n.dirocco@tech.leaseweb.com',
    url='http://developer.leaseweb.com',
    packages=find_packages(),
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_lswapi = lswapi.httpie:ApiAuthPlugin'
        ]
    },
    install_requires=[
        "requests"
    ],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities'
    ]
)
