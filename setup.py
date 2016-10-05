from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

# import the necessary files
#import pkgDir

setup(
    name='pkgName',
    version=pkgDir.__version__,
    url='git repo link',
    license='GNU General Public License',
    author='Jeremiah Coleman',
    tests_require=['nose', 'mongomock>=3.5.0'],
    install_requires=[],
    author_email='colemanja91@gmail.com',
    description='Put a short description here',
    #long_description=readme(),
    packages=['pkgName'],
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
    keywords = 'put some keywords here'
)
