# -*- coding: utf-8 -*-
from distutils.core import setup
import setuptools

setup(
    name='SQLAlchemy-Dao',
    version='1.2.2',
    author='Mengchen LEE',
    author_email='CooledCoffee@gmail.com',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries',
    ],
    description='Simple wrapper for sqlalchemy.',
    install_requires=[
        'decorated',
        'fixtures2',
        'inflection',
        'sqlalchemy',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    url='https://package-insights.appspot.com/packages/sqlalchemy-dao'
)
