import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('torpedo_sim')
    
    # Path to URDF
    urdf_file = os.path.join(pkg_share, 'models', 'tethys.urdf')
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    # Robot State Publisher (Reads URDF and Joint States)
    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

    # RViz2
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    )

    return LaunchDescription([rsp, rviz])
