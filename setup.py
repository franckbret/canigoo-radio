#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup script for canigoo-radio project"""

from setuptools import setup, find_packages
import os


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), 'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(os.path.join(here, 'CHANGELOG.rst'), 'r', encoding='utf-8') as changelog_file:
    changelog = changelog_file.read()

with open(os.path.join(here, 'VERSION'), 'r', encoding='utf-8') as version_file:
    version = version_file.read().strip()

requirements = [
    'passlib',
    'marshmallow',
    'psycopg2',
    'beets',
    'anyblok',
    'anyblok_pyramid',
    'pyramid_jinja2',
    'anyblok_pyramid_beaker',
    'anyblok-pyramid-rest-api',
    'cornice_swagger',
    'gunicorn',
]

test_requirements = []

setup(
    name='canigoo_radio',
    version=version,
    description="The project that runs canigoo.com music radio",
    long_description=readme + '\n\n' + changelog,
    author="Franck Bret",
    author_email='franckbret@gmail.com',
    url='https://github.com/franckbret/canigoo-radio',
    packages=find_packages(),
    entry_points={
        'bloks': [
            'canigoo_radio=canigoo_radio.canigoo_radio:Canigoo_radio'
            ]
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='canigoo-radio',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
