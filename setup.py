from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

# import the necessary files
import mlsm

setup(
    name='mlsm',
    version=mlsm.__version__,
    url='https://github.com/rh-marketingops/mlsm',
    license='GNU General Public License',
    author='Jeremiah Coleman',
    tests_require=['nose'],
    install_requires=['tqdm'],
    author_email='colemanja91@gmail.com',
    description='Implementation of multiple data science models',
    #long_description=readme(),
    packages=['mlsm'],
    include_package_data=True,
    platforms='any',
    test_suite = 'nose.collector',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
        ],
    keywords = 'data science lead scoring marketing automation'
)
