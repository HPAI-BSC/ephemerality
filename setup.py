import os
from setuptools import setup
import re

VERSION_FILE = "_version.py"
VERSION_REGEX = r"^__version__ = ['\"]([^'\"]*)['\"]"


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


version_lines = open(VERSION_FILE, 'r').read()
match = re.search(VERSION_REGEX, version_lines, re.M)
if match:
    version = match.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSION_FILE,))

setup(
    name='ephemerality',
    version=version,
    packages=['ephemerality'],
    url='https://github.com/HPAI-BSC/ephemerality',
    license='MIT',
    license_files=['./LICENSE'],
    author='HPAI BSC',
    author_email='dmitry.gnatyshak@bsc.es',
    description='Module for computing ephemerality metrics of temporal activity arrays.',
    long_description=read('README.md'),
    scripts=[],
    install_requires=[
        'numpy~=1.24.2',
        'fastapi~=0.95.1',
        'setuptools~=67.6.1',
        'pydantic~=1.10.7',
        'uvicorn~=0.21.1'
    ],
    extras_require={
        'test': [
            'requests~=2.28.2'
        ]
    }
)
