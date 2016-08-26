from setuptools import setup

setup(
    name='topics',
    version='0.1',
    description='Module analyzing topical contributions on Wikipedia',

    author='Kevin Schiroo',
    author_email='kjschiroo@gmail.com',

    packages=['topics'],
    install_requires=['mwxml', 'docopt']
)
