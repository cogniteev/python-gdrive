""" Setup file for distutils

"""

from distutils.core import setup
import os.path as osp
from setuptools import find_packages


__version__ = None
with open(osp.join('python_gdrive', '__init__.py')) as istr:
    for l in istr:
        if l.startswith('__version__ = '):
            exec(l)
            break

setup(
    name='python-gdrive',
    version=__version__,
    author='Tony Sanchez',
    author_email='tony@cogniteev.com',
    url='https://github.com/cogniteev/python-gdrive',
    download_url='https://github.com/cogniteev/python-gdrive/archive/master.zip',
    description='Gdrive REST api client',
    packages=find_packages(exclude=['tests']),
    license='Apache license version 2.0',
    platforms='OS Independent',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
        'Development Status :: 4 - Beta'
    ],
    install_requires='requests>=2.2.1'
)
