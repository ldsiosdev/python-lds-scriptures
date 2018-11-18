from distutils.core import setup

setup(
    name='python-lds-scriptures',
    version='1.0.0dev',
    packages=['scriptures',],
    license='MIT',
    description='Python package that parses LDS scripture URIs and formats them as human-readable strings.',
    long_description=open('README.md').read(),
    install_requires=[
        'memoize2>=0.1.1',
        'future>=0.17.1'
    ],
)
