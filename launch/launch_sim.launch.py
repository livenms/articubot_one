import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription

from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():

    package_name = "articubot_one"

    # Robot State Publisher
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory(package_name),
                "launch",
                "rsp.launch.py"
            )
        ),
        launch_arguments={
            "use_sim_time": "true"
        }.items()
    )

    # Gazebo Harmonic
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py"
            )
        ),
        launch_arguments={
            "gz_args": "-r empty.sdf"
        }.items()
    )

    bridge = Node(
    package="ros_gz_bridge",
    executable="parameter_bridge",
    arguments=[
        "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
        "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
        "/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V",
    ],
    output="screen"
)

    # Spawn robot
    spawn = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-topic",
            "robot_description",
            "-name",
            "my_bot"
        ],
        output="screen"
    )

    return LaunchDescription([
        rsp,
        gazebo,
        bridge,
        spawn,
    ])