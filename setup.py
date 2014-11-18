from setuptools import setup, find_packages

VERSION = '0.0.0'

setup(
    name='Hedgie',
    version=VERSION,
    description='Latency and fault tolerance for building distributed systems in Python.',
    license='MIT',

    packages=find_packages(),

    extras_require={
        ":'2.' in python_version or python_version=='3.0' or python_version=='3.1'": 'futures==2.2.0',
    },

    tests_require=[
        'pytest==2.6.4',
        'mock==1.0.1',
    ],
)
