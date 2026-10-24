import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_name = 'dummybot_description'
    pkg_path = get_package_share_directory(pkg_name)
    
    # 1. Locate the .urdf file directly
    urdf_file = os.path.join(pkg_path, 'urdf', 'dummybot.urdf')

    # 2. Read the file as standard text (No Xacro command needed!)
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()
    
    robot_description = {'robot_description': robot_desc}

    return LaunchDescription([
        # 3. Publish the robot model
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[robot_description],
            output='screen'
        ),
        # 4. Provide sliders to test the joints
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            output='screen'
        ),
        # 5. Open RViz to visualize
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen'
        )
    ])