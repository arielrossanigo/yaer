import ast
import re

from setuptools import find_packages, setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('yaer/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='yaer',
    version=version,
    description='Yet Another Experiment Runner',
    url='git@github.com:arielrossanigo/yaer.git',
    author='Ariel Rossanigo',
    author_email='arielrossanigo@gmail.com',
    packages=find_packages(),
    install_requires=[
        'click>=0.6.0',
    ],
    dependency_links=[
    ],
    setup_requires=[
        'pytest-runner>=2.11.0',
    ],
    tests_require=[
        'pytest>=3.2.0',
    ],
    extras_require={
        'dev': [
            'pycodestyle>=2.3.0',
            'flake8>=3.5.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'yaer = yaer.__main__:cli'
        ]
    },
)
