#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    'thunctor',
]
requires = []
version = '0.1.0'

setup(
    name='thunctor',
    version=version,
    description='Safe recursion with monads',
    author='Matt Neary',
    author_email='neary.matt@gmail.com',
    url='https://github.com/mattneary/Thunctor',
    packages=packages,
    package_data={'': ['LICENSE'], 'requests': []},
    package_dir={'thunctor': 'thunctor'},
    include_package_data=True,
    install_requires=requires,
    license='Apache 2.0',
    classifiers=(
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ),
    extras_require={},
)

