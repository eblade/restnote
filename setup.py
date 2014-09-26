#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup

name_ = 'restnote'
version_ = '0.0.3'

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "License :: OSI Approved :: MIT License",
    "Operating System :: POSIX",
    "Operating System :: POSIX :: Linux",
    "Topic :: Text Processing :: Markup",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Other Scripting Engines",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Text Processing :: Markup :: XML",
]

setup(
    name=name_,
    version=version_,
    author='Johan Egneblad',
    author_email='johan.egneblad@DELETEMEgmail.com',
    description='Rest scripting layer with notebook generation',
    license="MIT",
    url='https://github.com/eblade/'+name_,
    download_url=('https://github.com/eblade/%s/archive/v%s.tar.gz'
                  % (name_, version_)),
    packages=[],
    scripts=['bin/restnote'],
    classifiers = classifiers
)
