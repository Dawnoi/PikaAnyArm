from setuptools import find_packages, setup

package_name = 'nero_sdk'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    install_requires=['setuptools', 'numpy', 'scipy'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@example.com',
    description='Nero robot arm SDK wrapper',
    license='MIT',
    entry_points={},
)
