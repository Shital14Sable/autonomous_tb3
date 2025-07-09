# yellow_light_sdf=$HOME/.gazebo/models/yellow_light/model.sdf
# ros2 run self_driving_car_pkg spawner_node $red_light_sdf red_light 0.0 0.0
import sys
import rclpy
from gazebo_msgs.srv import SpawnEntity

def main():
    argv = sys.argv[1:]

    if len(argv) < 2:
        print("Usage: python3 spawner.py <model_path> <entity_name> [x] [y]")
        return
    rclpy.init()
    node = rclpy.create_node("SpawningNode")
    client = node.create_client(SpawnEntity, "/spawn_entity")
    if not client.service_is_ready():
        client.wait_for_service()
        node.get_logger().info("Waiting for spawn_entity service...")
        
    sdf_path = argv[0]
    request  = SpawnEntity.Request()
    request.name = argv[1]

    if len(argv) > 3:
        request.initial_pose.position.x = float(argv[2])
        request.initial_pose.position.y = float(argv[3])
    request.xml = open(sdf_path, "r").read()

    node.get_logger().info("Sending service request to '/spawn_entity'...")
    future = client.call_async(request)
    rclpy.spin_until_future_complete(node, future)
    if future.result() is not None:
        print('respose: %r' % future.result())
    else:
        raise RuntimeError('Exception while calling service: %r' % future.exception())

    node.get_logger().info("Entity spawned successfully.")
    node.destroy_node()
    rclpy.shutdown()    

if __name__ == "__main__":
    main()