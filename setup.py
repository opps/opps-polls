#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

import opps_poll



install_requires = ["Django==1.5",
                    "south>=0.7",
                    "django-tagging==0.3.1",
                    "django-wysiwyg-redactor==0.3.1",
                    "opps"]

classifiers = ["Development Status :: 4 - Beta",
               "Intended Audience :: Developers",
               "License :: OSI Approved :: MIT License",
               "Operating System :: OS Independent",
               "Framework :: Django",
               'Programming Language :: Python',
               "Programming Language :: Python :: 2.7",
               "Operating System :: OS Independent",
               "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
               'Topic :: Software Development :: Libraries :: Python Modules']

try:
    long_description = open('README.md').read()
except:
    long_description = opps_poll.__description__

setup(name='opps_poll',
        version=opps_poll.__version__,
        description=opps_poll.__description__,
        long_description=long_description,
        classifiers=classifiers,
        keywords='poll opps cms django apps magazines websites',
        author=opps_poll.__author__,
        author_email=opps_poll.__email__,
        url='http://oppsproject.org',
        download_url="https://github.com/oppsproject/opps.poll/tarball/master",
        license=opps_poll.__license__,
        packages=find_packages(exclude=('doc', 'docs',)),
        package_dir={'opps_poll': 'opps_poll'},
        install_requires=install_requires,
        include_package_data=True,)
