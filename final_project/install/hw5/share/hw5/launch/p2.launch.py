from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='hw5',
            executable='wallrider_v1',
            name='p2',
            parameters=[
                {'wall_dist': 0.5, 'clockwise': True}
            ]
        )        
    ])
