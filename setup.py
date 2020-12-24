#!/usr/bin/env python
from setuptools import setup

setup(
    name="richpanel-tap",
    version="0.1.0",
    description="Singer.io tap for extracting data",
    author="Stitch",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_richpanel"],
    install_requires=[
        # NB: Pin these to a more specific version for tap reliability
        "singer-python",
        "requests",
    ],
    entry_points="""
    [console_scripts]
    richpanel-tap=tap_richpanel:main
    """,
    packages=["tap_richpanel"],
    package_data = {
        "schemas": ["tap_richpanel/schemas/*.json"]
    },
    include_package_data=True,
)
