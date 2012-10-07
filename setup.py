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
    keywords='elevator leveldb database key-value',

    packages=['hurdles'],
    package_dir={'': '.'},
)
