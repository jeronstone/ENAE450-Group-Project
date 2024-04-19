from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='lab_package',
            executable='publish_vel',
            name='idk'
        )        
    ])