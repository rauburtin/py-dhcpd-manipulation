#!/usr/bin/env python
from setuptools import setup, find_packages
import os

_dirname = os.path.abspath(os.path.dirname(__file__))
README_PATH = os.path.join(_dirname, 'README.md')

description = '''\
Manipulates (add, retrieve, remove) reserved hosts within dhcpd config file.\
'''

if os.path.exists(README_PATH):
    long_description = open(README_PATH).read()
else:
    long_description = description

setup(name='py-dhcpd-manipulation',
    version='0.1',
    description=description,
    license='BSD',
    url='https://github.com/vencax/py-dhcpd-manipulation',
    author='vencax',
    author_email='info@vxk.cz',
    packages=find_packages(),
    install_requires=[],
    keywords="isc linux dhcpd manipulation",
    include_package_data=True,
)
