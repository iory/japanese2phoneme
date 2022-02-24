from __future__ import print_function

import shlex
import subprocess
import sys

from setuptools import find_packages
from setuptools import setup


version = "0.0.1"


if sys.argv[-1] == 'release':
    # Release via github-actions.
    commands = [
        'git tag v{:s}'.format(version),
        'git push origin master --tag',
    ]
    for cmd in commands:
        print('+ {}'.format(cmd))
        subprocess.check_call(shlex.split(cmd))
    sys.exit(0)


setup_requires = []

with open('requirements.txt') as f:
    install_requires = []
    for line in f:
        req = line.split('#')[0].strip()
        install_requires.append(req)

data_files = [
    'data/hiraganaChart.txt',
    'data/katakanaChart.txt',
]

setup(
    name="japanese2phoneme",
    version=version,
    description="A python library",
    author="iory",
    author_email="ab.ioryz@gmail.com",
    url="https://github.com/iory/japanese2phoneme",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    package_data={'japanese2phoneme': data_files},
    zip_safe=False,
    setup_requires=setup_requires,
    install_requires=install_requires,
)
