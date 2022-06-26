#!/usr/bin/env python3

from setuptools import setup

class About:
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]

    title = "lark_dynamic"
    description = "Dynamic grammar generator for Lark parsing toolkit"
    version = "1.0.3"
    author = "evtn"
    author_email = "courage@evtn.ru"
    license = "MIT"
    url = "https://github.com/courage-py/lark-dynamic"


with open("README.md") as file:
    long_description = file.read()

setup(
    name=About.title,
    version=About.version,
    author=About.author,
    author_email=About.author_email,
    url=About.url,
    py_modules=["lark_dynamic"],
    description=About.description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=About.license,
    install_requires=["lark"],
    classifiers=About.classifiers,
    python_requires=">=3.6",
)
