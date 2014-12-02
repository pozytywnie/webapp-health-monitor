from setuptools import find_packages
from setuptools import setup

setup(
    name='Webapp Health Monitor',
    version='0.1',
    author='Tomasz Wysocki',
    author_email='tomasz@pozytywnie.pl',
    url='https://github.com/pozytywnie/webapp-health-monitor',
    packages=find_packages(),
    scripts=[],
    license='MIT',
    description='',
    long_description=open('README.rst').read(),
    install_requires=[],
)
