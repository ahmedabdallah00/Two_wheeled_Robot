import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_name = 'dummybot_description'
    pkg_path = get_package_share_directory(pkg_name)

    urdf_file = os.path.join(pkg_path, 'urdf', 'dummybot.urdf')
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()
    robot_description = {'robot_description': robot_desc}

    # 1. Start Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ]),
        launch_arguments={'gz_args': '-r empty.sdf'}.items()
    )

    # 2. Publish the robot model
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[robot_description],
        output='screen'
    )

    # 3. Spawn the robot
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-name', 'dummybot', '-topic', 'robot_description', '-z', '0.5'],
        output='screen'
    )

    # 4. THE BRIDGE: Translates ROS /cmd_vel into Gazebo's language
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
        ],
        output='screen'
    )

    # 5. Your C++ driving script
    driver_node = Node(
        package='dummybot_description',
        executable='drive_circle',
        name='driver_node',
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_entity,
        bridge,
        driver_node
    ])