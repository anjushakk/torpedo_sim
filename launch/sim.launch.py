import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, AppendEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'torpedo_sim'
    pkg_share = get_package_share_directory(pkg_name)

    # 1. MODEL PATH: Points Gazebo to your 'models' folder in the install directory
    ign_resource_path = AppendEnvironmentVariable(
        name='IGN_GAZEBO_RESOURCE_PATH',
        value=os.path.join(pkg_share, 'models')
    )

    # 2. PLUGIN PATH: Ensures Gazebo Fortress finds the hydrodynamics/thruster plugins
    ign_plugin_path = AppendEnvironmentVariable(
        name='IGN_GAZEBO_SYSTEM_PLUGIN_PATH',
        value='/usr/lib/x86_64-linux-gnu/ign-gazebo-6/plugins'
    )

    # 3. GAZEBO SIMULATION: Loads your underwater world
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        # If you haven't created 'underwater_world.sdf' yet, change this to 'empty.sdf'
        # Change this line in your sim.launch.py
launch_arguments={'gz_args': '-r ' + os.path.join(pkg_share, 'worlds', 'underwater_world.sdf')}.items(),
    )

    # 4. SPAWN ROBOT: Spawns the Tethys model
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'tethys',
            '-file', os.path.join(pkg_share, 'models', 'tethys', 'model.sdf'),
            '-z', '-1.0' # Start 1 meter underwater
        ],
        output='screen'
    )
    

    # 5. BRIDGE: Maps ROS topics to Gazebo topics (e.g., cmd_vel to Thrusters)
    # Note: We will create the bridge.yaml next
    # Define the config path
    bridge_config = os.path.join(pkg_share, 'config', 'bridge.yaml')

    # BRIDGE: Use parameters to load the YAML file
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': bridge_config,
        }],
        output='screen'
    )
    

    return LaunchDescription([
        ign_resource_path,
        ign_plugin_path, 
        gz_sim,
        spawn_robot,
        bridge
    ])
