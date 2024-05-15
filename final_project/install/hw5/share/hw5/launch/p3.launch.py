from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='hw5',
            executable='wallrider_v2',
            name='p3',
        )        
    ])
