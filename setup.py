from setuptools import setup

version = __import__('hurdles').__version__

setup(
    name='Hurdles',
    version=version,
    license='MIT',

    description='A simple and yet powerful python benchmark framework.'
                       'Write unit benchs just like you\'d write unit tests.',

    author='Oleiade',
    author_email='tcrevon@gmail.com',
    url='http://github.com/oleiade/Hurdles',

    classifiers=[
        'Environment :: Unix-like Systems',
        'Programming Language :: Python',
        'Operating System :: Unix-like',
    ],
    keywords='hurldes benchmarks unit-benchmarks',

    packages=[
        'hurdles',
        'hurdles.referee',
        'hurdles.context',
    ],
    package_dir={'': '.'},

    install_requires=[
        'unittest2',
        'clint==0.3.1'
    ],

    zip_safe=False,

    # Setting up executable/main functions links
    entry_points={
        'console_scripts': [
            'hurdles = hurdles.referee.main:main',
        ]
    },
)
