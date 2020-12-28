#!/usr/bin/env python
from setuptools import setup

setup(
    name="richpanel-tap",
    version="0.1.0",
    description="Singer.io tap for extracting Richpanel data",
    author="Shubhanshu Chouhan",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_richpanel"],
    install_requires=[
        "singer-python",
        'python_graphql_client'
    ],
    entry_points="""
        [console_scripts]
        richpanel-tap=tap_richpanel:main
    """,
    packages=["tap_richpanel"],
    package_data = {
        "schemas": []
    },
    include_package_data=True,
)
