#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='hernrup-se-core',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'pelican>=3.0.0,<4.0.0',
        'livereload>=2.4.0',
        'Markdown>=2.6.2',
        'argh>=0.26.1'
    ],
    entry_points={
        'console_scripts': [
            'blog = hernrup_se_core.cli:main'
        ]
    }

)


