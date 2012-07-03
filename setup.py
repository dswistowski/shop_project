# coding=utf-8
from setuptools import setup, find_packages

setup(
    name = "tinyshop",
    version = "1.0",
    url = '',
    license = 'BSD',
    description = "Simple django shop app.",
    author = u'Damian Świstowski',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)

