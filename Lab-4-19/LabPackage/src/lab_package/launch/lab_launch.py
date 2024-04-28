from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='lab_package',
            executable='lab_publish_vel',
            name='idk',
            parameters=[
                {'wall_dist': 0.5, 'clockwise': True}
            ]
        )        
    ])
