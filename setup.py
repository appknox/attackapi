"""
attack api
"""
from setuptools import find_packages, setup

dependencies = ['click', 'redis']

description = 'attack api is a cli tool to find security vulnerabilities in an API.'
long_description = open('README.rst').read()

setup(
    name='attackapi',
    version='0.1.1',
    url='https://github.com/appknox/attackapi',
    license='BSD',
    author='Appknox',
    author_email='engineering@appknox.com',
    description=description,
    long_description=long_description,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'attackapi = attackapi.cli:cli',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
