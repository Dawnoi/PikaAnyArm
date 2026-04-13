import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    share_dir = get_package_share_directory('pika_remote_nero')

    declared_arguments = [
        DeclareLaunchArgument(
            'paramsFile',
            default_value=os.path.join(share_dir, 'config', 'nero_params.yaml'),
            description='Path to parameters file'
        ),
    ]
    parameter_file = LaunchConfiguration('paramsFile')

    locator_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('nero'), 'launch', 'start_single_nero.launch.py')
        ])
    )

    return LaunchDescription(declared_arguments + [
        locator_launch,
        Node(
            package='pika_remote_nero',
            executable='nero_FK.py',
            name='nero_FK',
            parameters=[{
                'index_name': '',
                'paramsFile': parameter_file
            }],
            respawn=True,
            output='screen'
        ),
        Node(
            package='pika_remote_nero',
            executable='nero_IK.py',
            name='nero_IK',
            parameters=[{
                'index_name': '',
                'paramsFile': parameter_file
            }],
            respawn=True,
            output='screen'
        ),
        Node(
            package='pika_remote_nero',
            executable='teleop_nero_publish.py',
            name='teleop_nero',
            parameters=[{
                'index_name': '',
                'return_zero_position': 'False'
            }],
            respawn=True,
            output='screen'
        ),
    ])
