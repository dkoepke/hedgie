from setuptools import setup, find_packages

VERSION = '0.0.0'

setup(
    name='Hedgie',
    version=VERSION,
    description='Latency and fault tolerance for building distributed systems in Python.',
    license='MIT',

    packages=find_packages(),

    tests_require=[
        'pytest==2.6.4',
        'mock==1.0.1',
    ],
)
