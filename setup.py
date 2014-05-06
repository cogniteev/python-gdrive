""" Setup file for distutils

"""

from distutils.core import setup

setup(
    name='python-gdrive',
    version='0.1',
    author='Tony Sanchez',
    author_email='mail.tsanchez@gmail.com',
    url='https://github.com/tsanch3z/python-gdrive',
    download_url='https://github.com/tsanch3z/python-gdrive/archive/master.zip',
    description='Gdrive REST api client',
    packages=['python_gdrive'],
    license='GPLv2',
    platforms='OS Independent',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
        'Development Status :: 4 - Beta'
    ],
    install_requires='requests>=2.2.1'
)
