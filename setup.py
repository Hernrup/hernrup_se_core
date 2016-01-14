#!/usr/bin/env python
from setuptools import setup, find_packages, Command
from os import path
import pip


def readme():
    with open(path.join(path.abspath(path.dirname(__file__)),
                        'README.rst')) as f:
        return f.read()


setup_requires = [
    'flake8>=2.1.0',
    'describe-it>=1.1.0',
    'nose>=1.3.3',
    'PyHamcrest>=1.8.1',
    'wheel>=0.22.0',
]

install_requires = [
    'pelican>=3.0.0,<4.0.0',
    'livereload>=2.4.0'
    'Markdown>=2.6.2'
]


class InstallSetupRequirementsCommand(Command):
    description = "run my command"
    user_options = tuple()

    def initialize_options(self):
        pass

    def finalize_options(self):
         pass

    def install_package(self, package):
        pip.main(['install', package])

    def run(self):
        for p in setup_requires:
            self.install_package(p)

setup(
    name='hernrup-se-core',
    version='0.0.1',
    packages=find_packages(),
    install_requires=install_requires,
    setup_requires=setup_requires,
    dependency_links=[],
    entry_points={
        'console_scripts': [
            'blog = core.cli:main'
        ]
    },
    cmdclass={
        'pylint': InstallSetupRequirementsCommand,
    },

)


