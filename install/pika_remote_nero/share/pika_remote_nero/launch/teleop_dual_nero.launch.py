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

    # 启动 RViz 和 robot_state_publisher
    display_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('nero_description'), 'launch', 'display_xacro.launch.py')
        ])
    )

    return LaunchDescription(declared_arguments + [
        # 启动 RViz 和 robot_state_publisher
        display_launch,
        
        # 左臂 FK 节点
        Node(
            package='pika_remote_nero',
            executable='nero_FK.py',
            name='nero_FK_l',
            parameters=[{
                'index_name': '_l',
                'paramsFile': parameter_file
            }],
            respawn=True,
            output='screen'
        ),
        # 左臂 IK 节点
        Node(
            package='pika_remote_nero',
            executable='nero_IK.py',
            name='nero_IK_l',
            parameters=[{
                'index_name': '_l',
                'paramsFile': parameter_file
            }],
            respawn=True,
            output='screen'
        ),
        # 左臂遥操作节点
        Node(
            package='pika_remote_nero',
            executable='teleop_nero_publish.py',
            name='teleop_nero_l',
            parameters=[{
                'index_name': '_l'
            }],
            respawn=True,
            output='screen'
        ),

        
        # 右臂 FK 节点
        Node(
            package='pika_remote_nero',
            executable='nero_FK.py',
            name='nero_FK_r',
            parameters=[{
                'index_name': '_r',
                'paramsFile': parameter_file
            }],
            respawn=True,
            output='screen'
        ),
        # 右臂 IK 节点
        Node(
            package='pika_remote_nero',
            executable='nero_IK.py',
            name='nero_IK_r',
            parameters=[{
                'index_name': '_r',
                'paramsFile': parameter_file
            }],
            respawn=True,
            output='screen'
        ),
        # 右臂遥操作节点
        Node(
            package='pika_remote_nero',
            executable='teleop_nero_publish.py',
            name='teleop_nero_r',
            parameters=[{
                'index_name': '_r'
            }],
            respawn=True,
            output='screen'
        ),
    ])
