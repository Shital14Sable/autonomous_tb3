from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    launch_file_dir = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'launch')
    hotel_path = os.path.join(get_package_share_directory('autonomous_tb3'), 'world', 'hotel', 'model.sdf')
    # print("Hotel SDF path:", hotel_path)
    table_path = os.path.join(get_package_share_directory('autonomous_tb3'), 'models', 'table', 'model.sdf')
    package_gazebo_ros = get_package_share_directory('gazebo_ros')
    config_dir = os.path.join(get_package_share_directory('autonomous_tb3'), 'config')
    map_file = os.path.join(config_dir, 'hotel_map.yaml')
    params_file = os.path.join(config_dir, 'tb3_nav_params.yaml')
    # map_config = os.path.join(config_dir, 'mapping.rviz')
    nav_config = os.path.join(config_dir, 'tb3_nav.rviz')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    x_pose = LaunchConfiguration('x_pose', default='-0.232612')
    y_pose = LaunchConfiguration('y_pose', default='-5.632428')


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

    hotel_spawner = Node(
        package='autonomous_tb3',
        output='screen',
        executable='sdf_spawner',
        name='hotel_spawner',
        arguments=[hotel_path,"hotel", "0.0", "0.0"]
    )

    table_1_spawner = Node(
        package='autonomous_tb3',
        output='screen',
        executable='sdf_spawner',
        name='table_1_spawner',
        arguments=[table_path,"table_1", "-3.514500", "-1.425685"]
    )

    table_2_spawner = Node(
        package='autonomous_tb3',
        output='screen',
        executable='sdf_spawner',
        name='table_2_spawner',
        arguments=[table_path,"table_2", "-3.425865", "3.461600"]
    )

    table_3_spawner = Node(
        package='autonomous_tb3',
        output='screen',
        executable='sdf_spawner',
        name='table_3_spawner',
        arguments=[table_path,"table_3", "3.428090", "3.448285"]
    )

    table_4_spawner = Node(
        package='autonomous_tb3',
        output='screen',
        executable='sdf_spawner',
        name='table_4_spawner',
        arguments=[table_path,"table_4", "3.480000", "-1.488200"]
    )


    hotel_mapping = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('slam_toolbox'), 'launch', 'online_async_launch.py')
        ),
    )

    hotel_nav = IncludeLaunchDescription(
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
            # arguments=['-d', map_config],
            arguments=['-d', nav_config]

        )


    ld = LaunchDescription()

    # Add the commands to the launch description
    ld.add_action(gzserver_cmd)
    ld.add_action(gzclient_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(spawn_turtlebot_cmd)

    ld.add_action(hotel_spawner)

    ld.add_action(table_1_spawner)
    ld.add_action(table_2_spawner)
    ld.add_action(table_3_spawner)
    ld.add_action(table_4_spawner)

    # ld.add_action(hotel_mapping)
    ld.add_action(rviz_node)
    ld.add_action(hotel_nav)


    return ld
