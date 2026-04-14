from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Declare the launch arguments
    can_left_port_arg = DeclareLaunchArgument(
        'can_left_port',
        default_value='can_left',
        description='CAN left port to be used by the Nero node.'
    )
    can_right_port_arg = DeclareLaunchArgument(
        'can_right_port',
        default_value='can_right',
        description='CAN right port to be used by the Nero node.'
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

    # Define the left nero node
    nero_left_node = Node(
        package='nero',
        executable='nero_single_ctrl',
        name='nero_left_ctrl_node',
        output='screen',
        parameters=[{
            'can_port': LaunchConfiguration('can_left_port'),
            'auto_enable': LaunchConfiguration('auto_enable'),
            'rviz_ctrl_flag': LaunchConfiguration('rviz_ctrl_flag'),
            'girpper_exist': LaunchConfiguration('girpper_exist'),
            'nero_name': 'left',
        }],
        remappings=[
            ('pos_cmd', '/pos_left_cmd'),
            ('/puppet/joint_left', '/joint_states_single_l'),
            ('joint_ctrl_single', '/joint_states_gripper_l'),
        ]
    )

    # Define the right nero node
    nero_right_node = Node(
        package='nero',
        executable='nero_single_ctrl',
        name='nero_right_ctrl_node',
        output='screen',
        parameters=[{
            'can_port': LaunchConfiguration('can_right_port'),
            'auto_enable': LaunchConfiguration('auto_enable'),
            'rviz_ctrl_flag': LaunchConfiguration('rviz_ctrl_flag'),
            'girpper_exist': LaunchConfiguration('girpper_exist'),
            'nero_name': 'right',
        }],
        remappings=[
            ('pos_cmd', '/pos_right_cmd'),
            ('/puppet/joint_right', '/joint_states_single_r'),
            ('joint_ctrl_single', '/joint_states_gripper_r'),
        ]
    )

    # Return the LaunchDescription
    return LaunchDescription([
        can_left_port_arg,
        can_right_port_arg,
        auto_enable_arg,
        rviz_ctrl_flag_arg,
        girpper_exist_arg,
        nero_left_node,
        nero_right_node
    ])
