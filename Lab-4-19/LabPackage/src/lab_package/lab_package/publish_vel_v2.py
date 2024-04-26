import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np

PI = np.pi
D = 0.5
NORM = PI / 2
SMOOTHING = 0.5
CLIP = 5
FWD = PI
FWD_ANGLE = PI / 4

TO_RADIANS = PI / 360

distance = 0.5
lidar_alpha = 15
lidar_alpha_buffer = 0.1
distance_buffer = 0.1

class LabNode(Node):
    def __init__(self):
        super().__init__('lab_4_26_v2')

        self.scan_subscriber = self.create_subscription(LaserScan,'/scan',self.scan_subscriber_handler,10)
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(.1, self.timer_callback)
    
    def timer_callback(self):
        twist = Twist()
        if (!self.ranges) return
        a = np.array(self.ranges)
        a = np.convolve(np.clip(a, 0, CLIP), [0.2] * 5, mode = 'same')
        m = np.argmin(a)
        theta = m * TO_RADIANS
        twist.angular.z = (theta - NORM) * SMOOTHING
        twist.linear.x = 0.5 if self.ranges[m] < D and (FWD - FWD_ANGLE) < theta < FWD + FWD_ANGLE) else 0
        self.cmd_vel_publisher.publish(twist)
    # ranges[0] -> back
    # ranges[360] -> front
    # ranges[180] -> right
    # ranges[540] -> left
    def scan_subscriber_handler(self, data):
        self.ranges = data.ranges

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