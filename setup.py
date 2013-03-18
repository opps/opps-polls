#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

from opps import polls


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
    long_description = polls.__description__

setup(name='opps-polls',
        namespace_packages=['opps'],
        version=polls.__version__,
        description=polls.__description__,
        long_description=long_description,
        classifiers=classifiers,
        keywords='poll opps cms django apps magazines websites',
        author=polls.__author__,
        author_email=polls.__email__,
        url='http://oppsproject.org',
        download_url="https://github.com/oppsproject/opps-polls/tarball/master",
        license=polls.__license__,
        packages=find_packages(exclude=('doc', 'docs',)),
        package_dir={'opps': 'opps'},
        install_requires=install_requires,
        include_package_data=True,
        package_data={
           'polls': ['templates/*']
        })
