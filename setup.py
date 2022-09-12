# -*- coding: utf-8 -*-

import sys

if 'bdist_wheel' in sys.argv:
    # to build wheel, use 'python setup.py sdist bdist_wheel'
    from setuptools import setup
else:
    from distutils.core import setup # 'python setup.py install'

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='chncal',
    version='2.0.1',
    description='Check if some day is holiday in china.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Genlovy Hoo',
    author_email='genlovhyy@163.com',
    url='https://github.com/Genlovy-Hoo/chncal',
    license='MIT License',
    install_requires=[],
    packages=['chncal',
              'chncal.data'],
)
