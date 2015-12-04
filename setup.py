from setuptools import setup
from codecs import open
from os import path

BASE_DIR = path.abspath(path.dirname(__file__))

with open(path.join(BASE_DIR, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='jsontool',
    version='0.2.1',
    description='`jsontool` is utility to fighting with JSON files using CLI',
    long_description=long_description,
    url='http://msztolcman.github.io/jsontool/',
    author='Marcin Sztolcman',
    author_email='marcin@urzenia.net',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=['argparse', 'pygments'],
    py_modules=['jsontool'],

    keywords='json processing grep sort',

    entry_points={
        'console_scripts': [
            'jsontool=jsontool:main',
        ],
    },
)

