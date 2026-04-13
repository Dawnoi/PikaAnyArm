from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Declare the launch arguments
    can_port_arg = DeclareLaunchArgument(
        'can_port',
        default_value='can0',
        description='CAN port to be used by the Nero node.'
    )
    auto_enable_arg = DeclareLaunchArgument(
        'auto_enable',
        default_value='true',
        description='Automatically enable the Nero node.'
    )
    
    rviz_ctrl_flag_arg = DeclareLaunchArgument(
        'rviz_ctrl_flag',
        default_value='false',
        description='Start rviz flag.'
    )
    
    girpper_exist_arg = DeclareLaunchArgument(
        'girpper_exist',
        default_value='true',
        description='gripper'
    )

    nero_name_arg = DeclareLaunchArgument(
        'nero_name',
        default_value='left',
        description='Nero arm name (left/right).'
    )

    # Define the nero_ctrl_single_node
    nero_ctrl_node = Node(
        package='nero',
        executable='nero_single_ctrl',
        name='nero_ctrl_single_node',
        output='screen',
        parameters=[{
            'can_port': LaunchConfiguration('can_port'),
            'auto_enable': LaunchConfiguration('auto_enable'),
            'rviz_ctrl_flag': LaunchConfiguration('rviz_ctrl_flag'),
            'girpper_exist': LaunchConfiguration('girpper_exist'),
            'nero_name': LaunchConfiguration('nero_name'),
        }],
        remappings=[
            ('joint_ctrl_single', '/joint_states_gripper'),
            ('/puppet/joint_left', '/joint_states_single'),
        ]
    )

    # Return the LaunchDescription
    return LaunchDescription([
        can_port_arg,
        auto_enable_arg,
        rviz_ctrl_flag_arg,
        girpper_exist_arg,
        nero_name_arg,
        nero_ctrl_node
    ])
