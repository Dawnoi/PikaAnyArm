from setuptools import setup
import os
from glob import glob

package_name = 'pika_remote_nero'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Pika Team',
    maintainer_email='pika@example.com',
    description='Nero robot arm teleoperation package for Pika system',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'nero_FK = pika_remote_nero.scripts.nero_FK:main',
            'nero_IK = pika_remote_nero.scripts.nero_IK:main',
            'teleop_nero_publish = pika_remote_nero.scripts.teleop_nero_publish:main',
        ],
    },
)
