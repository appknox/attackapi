"""
attack api
"""
from setuptools import find_packages, setup

dependencies = ['click']

setup(
    name='attackapi',
    version='0.1.0',
    url='https://github.com/chillaranand/attackapi',
    license='BSD',
    author='chillar anand',
    author_email='vincent@3rdcloud.com',
    description='attack api',
    long_description=__doc__,
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
