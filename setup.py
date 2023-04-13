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
    packages=['ephemerality', 'testing'],
    url='https://github.com/HPAI-BSC/ephemerality',
    license='MIT',
    author='HPAI BSC',
    author_email='dmitry.gnatyshak@bsc.es',
    description='Module for computing ephemerality metrics of temporal arrays.',
    long_description=read('README.md')
)
