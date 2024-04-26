from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'lab_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jstone14',
    maintainer_email='jstone14@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "lab_publish_vel = lab_package.publish_vel:main",
            "lab_publish_vel_v2 = lab_package.publish_vel_v2:main"
        ],
    },
)
