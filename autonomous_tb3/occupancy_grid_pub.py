import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
from std_msgs.msg import String
from std_msgs.msg import Header
import numpy as np

class OccupancyGridPub(Node):
    def __init__(self):
        super().__init__('OccupancyGrid_pub_node')
        self.grid_publisher_ = self.create_publisher(OccupancyGrid, 'map', 10)
        self.timer = self.create_timer(0.5, self.OG_pub_callback)

    def OG_pub_callback(self):
        occupancy_grid_msg = OccupancyGrid()
        occupancy_grid_msg.header = Header()
        occupancy_grid_msg.header.stamp = self.get_clock().now().to_msg()     
        occupancy_grid_msg.header.frame_id = 'map_frame'

        occupancy_grid_msg.info.resolution = 1.0
        occupancy_grid_msg.info.width = 2
        occupancy_grid_msg.info.height = 2

        occupancy_grid_msg.info.origin.position.x = 0.0
        occupancy_grid_msg.info.origin.position.y = 0.0
        occupancy_grid_msg.info.origin.position.z = 0.0
        
        occupancy_grid_msg.data = np.array([1,1,1,1], dtype=np.int8).tolist()


        self.grid_publisher_.publish(occupancy_grid_msg)

def main(args=None):
    rclpy.init(args=args)
    OG_publisher = OccupancyGridPub()
    rclpy.spin(OG_publisher)
    rclpy.shutdown()


if __name__ == "__main__":
    main()