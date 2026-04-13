import os
import subprocess
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_name = 'nero_description'
    pkg_share = get_package_share_directory(pkg_name)
    xacro_file = os.path.join(pkg_share, 'urdf', 'nero_dual_arm_with_gripper_description.xacro')
    rviz_config = os.path.join(pkg_share, 'rviz', 'rviz.config')

    declared_arguments = [
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation clock time'
        ),
        DeclareLaunchArgument(
            'rvizconfig',
            default_value=rviz_config,
            description='Absolute path to rviz config file'
        ),
    ]

    # 使用xacro生成URDF
    import shutil
    xacro_path = shutil.which('xacro')
    if xacro_path is None:
        raise RuntimeError("'xacro' not found. Install with: sudo apt install ros-humble-xacro")
    robot_description = subprocess.check_output([xacro_path, xacro_file]).decode('utf-8')

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'robot_description': robot_description,
        }],
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
    )

    return LaunchDescription(declared_arguments + [
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node,
    ])