#!/usr/bin/env python
# -*- coding: utf-8 -*-

options = {
    "name":         "stackpath",
    "version":      "0.0.1",
    "description":  "A Python REST Client for StackPath REST Web Services. This package is forked from https://github.com/MaxCDN/python-maxcdn/",
    "author":       "Kouichi Nihsizawa",
    "author_email": "kouichi.nishizawa+github@gmail.com",
    "license":      "MIT",
    "keywords":     "StackPath CDN API REST",
    "packages":     ['stackpath'],
    "url":          'http://github.com/koty/python-stackpath'
}

install_requires = [
    "requests",
    "requests_oauthlib",
    "certifi"
]
tests_require = [
    "nose",
    "mock"
]
include_package_data = True

try:
    from setuptools import setup
    options["install_requires"] = install_requires
    options["include_package_data"] = include_package_data
    options["tests_require"] = tests_require
    setup(**options)

except ImportError:
    print("ERROR: setuptools wasn't found, please install it")
