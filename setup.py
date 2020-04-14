#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read().splitlines()

# with open('testing_requirements.txt') as requirements_file:
    # testing_requirements = requirements_file.read().splitlines()


setup(
    name='tcpwave-client',
    version='1.0.1',
    description="Client for interacting with Tcpwave's IPAM",
    license='Apache',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    author="Suman Saurabh",
    author_email='saurabh.suman@tcpwave.com',
    url='https://github.com/TCPWAVE/tims-python-client',
    download_url='https://github.com/TCPWAVE/tims-python-client/archive/master.zip',
    packages=[
        'client',
    ],
    package_dir={'client': 'client'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords=['tcpwave-client', 'ipam-client', 'tcpwave'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    # test_suite='tests',
    # tests_require=testing_requirements
)
