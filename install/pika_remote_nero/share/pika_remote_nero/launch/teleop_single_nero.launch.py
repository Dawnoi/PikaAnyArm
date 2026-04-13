import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
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
        DeclareLaunchArgument(
            'index_name',
            default_value='',
            description='Index name for multi-arm setup'
        ),
    ]
    parameter_file = LaunchConfiguration('paramsFile')
    index_name = LaunchConfiguration('index_name')

    return LaunchDescription(declared_arguments + [
        # Nero 硬件控制节点 (发布 /joint_states_single{index})
        Node(
            package='nero',
            executable='nero_single_ctrl',
            name='nero_ctrl_single_node',
            parameters=[{
                'can_port': 'can0',
                'auto_enable': True,
                'rviz_ctrl_flag': False,
                'girpper_exist': True,
                'nero_name': 'left',
            }],
            remappings=[
                ('/puppet/joint_left', '/joint_states_single'),
            ],
            output='screen'
        ),
        # Nero FK 节点
        Node(
            package='pika_remote_nero',
            executable='nero_FK.py',
            name='nero_FK',
            parameters=[{
                'index_name': index_name,
                'paramsFile': parameter_file
            }],
            remappings=[
                ('/joint_states_single', '/joint_states_single'),
            ],
            respawn=True,
            output='screen'
        ),
        # Nero IK 节点
        Node(
            package='pika_remote_nero',
            executable='nero_IK.py',
            name='nero_IK',
            parameters=[{
                'index_name': index_name,
                'paramsFile': parameter_file
            }],
            remappings=[
                ('/joint_states_single', '/joint_states_single'),
            ],
            respawn=True,
            output='screen'
        ),
        # 遥操作发布节点
        Node(
            package='pika_remote_nero',
            executable='teleop_nero_publish.py',
            name='teleop_nero',
            parameters=[{
                'index_name': index_name
            }],
            respawn=True,
            output='screen'
        ),
    ])
