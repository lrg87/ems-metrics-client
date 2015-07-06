from setuptools import setup, find_packages

__author__ = 'xuemingli'

def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name='ems-metrics-client',
    version="0.1.0",
    license='apache-2',
    author='comyn',
    author_email='me@xueming.li',
    description='EMS metrics client',
    long_description=readme(),
    url='https://git.elenet.me/opdev/ems-metrics-client',
    download_url='https://github.com/eleme/ems-metrics-client/tarball/v0.0.2'
    packages=['ems'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
)
