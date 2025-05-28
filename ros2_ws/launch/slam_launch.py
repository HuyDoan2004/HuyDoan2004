from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='uart_control',
            executable='uart_control',
            output='screen'
        ),
        Node(
            package='ultrasonic_sensor',
            executable='ultrasonic_sensor',
            output='screen'
        ),
        Node(
            package='fake_odometry',
            executable='fake_odometry',
            output='screen'
        ),
        Node(
            package='slam_toolbox',
            executable='sync_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[
                {'use_sim_time': False},
                {'slam_params_file': 'config/slam_params.yaml'},
                {'map_save_period': 60.0}
            ]
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', 'config/rviz_config.rviz']
        )
    ])
