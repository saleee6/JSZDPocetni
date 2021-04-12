import codecs
import os

from setuptools import find_packages, setup

PACKAGE_NAME = "JRG"
VERSION = "1.0.0"
AUTHOR = "Team 2"
AUTHOR_EMAIL = "team2@gmail.com"
DESCRIPTION = "Simple DSL which is used to generate Java SpringBoot and React.js project."
KEYWORDS = "DSL, React, Java SpringBoot"
LICENSE = "MIT"
URL = "https://github.com/AleksasGitHub/JSD"

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    keywords=KEYWORDS,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["*.tx"]},
    install_requires=["textX[cli]"],
    entry_points={
        'textx_languages': [
            'full_stack_lang = JRG:full_stack_lang',
          ],
        'textx_generators': [
            'full_stack_gen = JRG:full_stack_gen',
          ]
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)