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

        # 左臂硬件控制节点
        Node(
            package='nero',
            executable='nero_single_ctrl',
            name='nero_ctrl_single_node_l',
            parameters=[{
                'can_port': 'can_left',
                'auto_enable': True,
                'rviz_ctrl_flag': False,
                'girpper_exist': True,
                'nero_name': 'left',
            }],
            remappings=[
                ('/puppet/joint_left', '/joint_states_single_l'),
                ('joint_ctrl_single', '/joint_states_l'),
            ],
            output='screen'
        ),

        # 左臂 FK 节点
        Node(
            package='pika_remote_nero',
            executable='nero_FK.py',
            name='nero_FK_l',
            parameters=[{
                'index_name': '_l',
                'paramsFile': parameter_file
            }],
            remappings=[
                ('/joint_states_single', '/joint_states_single_l'),
            ],
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
            remappings=[
                # IK 发布 /joint_states_l，直接匹配硬件节点订阅的话题
                ('/joint_states', '/joint_states_l'),
                ('/joint_states_single', '/joint_states_single_l'),
            ],
            respawn=True,
            output='screen'
        ),
        # 左臂遥操作节点
        Node(
            package='pika_remote_nero',
            executable='teleop_nero_publish.py',
            name='teleop_nero_l',
            parameters=[{
                'index_name': '_l',
                'return_zero_position': 'False'
            }],
            remappings=[
                ('/joint_states', '/joint_states_l'),
            ],
            respawn=True,
            output='screen'
        ),

        # 右臂硬件控制节点
        Node(
            package='nero',
            executable='nero_single_ctrl',
            name='nero_ctrl_single_node_r',
            parameters=[{
                'can_port': 'can_right',
                'auto_enable': True,
                'rviz_ctrl_flag': False,
                'girpper_exist': True,
                'nero_name': 'right',
            }],
            remappings=[
                ('/puppet/joint_right', '/joint_states_single_r'),
                ('joint_ctrl_single', '/joint_states_r'),
            ],
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
            remappings=[
                ('/joint_states_single', '/joint_states_single_r'),
            ],
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
            remappings=[
                # IK 发布 /joint_states_r，直接匹配硬件节点订阅的话题
                ('/joint_states', '/joint_states_r'),
                ('/joint_states_single', '/joint_states_single_r'),
            ],
            respawn=True,
            output='screen'
        ),
        # 右臂遥操作节点
        Node(
            package='pika_remote_nero',
            executable='teleop_nero_publish.py',
            name='teleop_nero_r',
            parameters=[{
                'index_name': '_r',
                'return_zero_position': 'False'
            }],
            remappings=[
                ('/joint_states', '/joint_states_r'),
            ],
            respawn=True,
            output='screen'
        ),
    ])
