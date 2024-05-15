from setuptools import find_packages, setup
import os
from glob import glob


package_name = 'maze_simulation'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'worlds'), glob(os.path.join('worlds', '*.world*'))),
        (os.path.join('share', package_name, 'models','tb3_4walls'), glob(os.path.join('models','tb3_4walls','*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='adi',
    maintainer_email='adi@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
