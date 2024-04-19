import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class LabNode(Node):
    def __init__(self):
        super().__init__('lab_4_19')

        self.scan_subscriber = self.create_subscription(LaserScan,'/scan',self.scan_subscriber_handler,10)
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        self.timer = self.create_timer(.1, self.timer_callback)
    
    def timer_callback(self):
        pass

    def scan_subscriber_handler(self, data):
        self.print("Lidar @ 0 deg: " + str(data.ranges[0]))
        self.print("Lidar @ 90 deg: " + str(data.ranges[90]))
        self.print("Lidar @ 180 deg: " + str(data.ranges[180]))
        self.print("Lidar @ 270 deg: " + str(data.ranges[270]))

    # logger print wrapper for debugging
    def print(self, str):
        self.get_logger().info(str)

def main(args=None):
    rclpy.init(args=args)

    labnode = LabNode()

    rclpy.spin(labnode)
    
    labnode.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()