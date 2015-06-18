from setuptools import find_packages
from setuptools import setup

setup(
    name='webapp-health-monitor',
    version='0.1.5',
    author='Tomasz Wysocki',
    author_email='tomasz@pozytywnie.pl',
    url='https://github.com/pozytywnie/webapp-health-monitor',
    packages=find_packages(),
    license='MIT',
    description='',
    long_description=open('README.rst').read(),
    install_requires=[],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'webapp_health_monitor='
            'webapp_health_monitor.scripts:webapp_health_monitor',
        ]
    },
    zip_safe=False,
)
