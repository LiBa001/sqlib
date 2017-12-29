from setuptools import setup, find_packages

setup(
    name='sqlib',
    version='0.0.1',
    description='A wrapper for sqlite3 to keep your code free from SQL.',
    long_description='content will follow',
    url='https://github.com/LiBa001/sqlib',
    author='Linus Bartsch',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.6'
    ],
    keywords='sqlite sql database wrapper',
    install_requires=[],
    packages=find_packages(),
    data_files=None
)
