from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'autonomous_tb3'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
        (os.path.join('share', package_name, 'world/maze'), glob('world/maze/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='nightowl',
    maintainer_email='shital14sable@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'occupancy_grid_pub = autonomous_tb3.occupancy_grid_pub:main',
            'sdf_spawner = autonomous_tb3.spawn_entity:main',
            'maze_solver = autonomous_tb3.maze_solver:main'
        ],
    },
)
