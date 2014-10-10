import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.txt')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='ilmtools',
    version='0.1',
    packages=['ilmtools'],
    include_package_data=True,
    license='GPL License',  # example license
    description='Tools for simulating and performing inference of individual level infectious disease transmission models',
    long_description=README,
    url='http://github.com/jangevaa/ilmtools',
    author='Justin Angevaare',
    author_email='jangevaa@uoguelph.ca',
    classifiers=[
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)