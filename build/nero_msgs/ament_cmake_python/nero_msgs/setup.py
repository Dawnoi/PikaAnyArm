from setuptools import find_packages
from setuptools import setup

setup(
    name='nero_msgs',
    version='1.0.0',
    packages=find_packages(
        include=('nero_msgs', 'nero_msgs.*')),
)
