from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    launch_file_dir = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'launch')
    maze_path = os.path.join(get_package_share_directory('autonomous_tb3'), 'world', 'maze', 'model.sdf')
    package_gazebo_ros = get_package_share_directory('gazebo_ros')
    config_dir = os.path.join(get_package_share_directory('autonomous_tb3'), 'config')
    map_file = os.path.join(config_dir, 'maze.yaml')
    params_file = os.path.join(config_dir, 'tb3_nav_params.yaml')
    rviz_config = os.path.join(config_dir, 'tb3_nav.rviz')

    use_sim_time = LaunchConfiguration('use_sim_time:', default='true')
    x_pose = LaunchConfiguration('x_pose', default='-3.4')
    y_pose = LaunchConfiguration('y_pose', default='-6.5')


    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(package_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
    )

    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(package_gazebo_ros, 'launch', 'gzclient.launch.py')
        ),
    )

    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, 'robot_state_publisher.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    spawn_turtlebot_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, 'spawn_turtlebot3.launch.py')
        ),
        launch_arguments={
            'x_pose': x_pose,
            'y_pose': y_pose
        }.items()
    )

    maze_spawner = Node(
        package='autonomous_tb3',
        output='screen',
        executable='sdf_spawner',
        name='maze_spawner',
        arguments=[maze_path,"b", "0.0", "0.0"]
    )


    maze_mapping = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('slam_toolbox'), 'launch', 'online_async_launch.py')
        ),
    )

    maze_nav = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory('nav2_bringup'), '/launch', '/bringup_launch.py']),
        launch_arguments={
            'map':map_file,
            'params_file': params_file}.items(),
    )

    rviz_node = Node(
            package='rviz2',
            output='screen',
            executable='rviz2',
            name='rviz2_node',
            arguments=['-d', rviz_config]
        )


    ld = LaunchDescription()

    # Add the commands to the launch description
    ld.add_action(gzserver_cmd)
    ld.add_action(gzclient_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(spawn_turtlebot_cmd)
    ld.add_action(maze_spawner)
    ld.add_action(maze_mapping)
    ld.add_action(rviz_node)
    ld.add_action(maze_nav)


    return ld



# def generate_launch_description():
#     config_dir = os.path.join(get_package_share_directory('autonomous_tb3'), 'config')
#     map_file = os.path.join(config_dir, 'tb3_world.yaml')
#     params_file = os.path.join(config_dir, 'tb3_nav_params.yaml')
#     rviz_config = os.path.join(config_dir, 'tb3_nav.rviz')
#     return LaunchDescription([
#         # Bringing our robot
#        # Integrating Nav2 stack
#         IncludeLaunchDescription(PythonLaunchDescriptionSource
#                         ([get_package_share_directory('nav2_bringup'), '/launch', '/bringup_launch.py']),
#                         launch_arguments={
#                             'map' : map_file,
#                             'params_file' : params_file}.items()
#         ),
        
#         #  Rviz2 bringup
#         Node(
#             package='rviz2',
#             output='screen',
#             executable='rviz2',
#             name='rviz2_node',
#             arguments=['-d', rviz_config]
#         )
#     ])