from setuptools import setup, find_packages

setup(
    name='lswapi',
    version='0.0.9',
    description='a python library for easy leaseweb api access',
    author='Nico Di Rocco',
    author_email='n.dirocco@tech.leaseweb.com',
    url='http://developer.leaseweb.com',
    packages=find_packages(),
    install_requires=[
        "requests"
    ]
)
