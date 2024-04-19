import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class LabNode(Node):
    def __init__(self):
        super().__init__('lab_4_19')

        self.scan_subscriber = self.create_subscription(LaserScan,'/scan',self.scan_subscriber_handler,10)
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        self.front_lidar_val = None
        self.turning = False
        self.turn_c = 0

        self.timer = self.create_timer(.1, self.timer_callback)
    
    def timer_callback(self):
        pose = Twist()

        if not self.turning:
            if not self.front_lidar_val or self.front_lidar_val > 0.75:
                pose.linear.x = 0.25
            else:
                pose.linear.x = 0.0
                self.turning = True
        else:
            if self.turn_c < 3:
                pose.angular.z = 3.14/6.0
                self.turn_c += 1
            else:
                pose.angular.z = 0
                self.turn_c = 0
                self.turning = False            
        
        self.cmd_vel_publisher.publish(pose)


    # ranges[0] -> back
    # ranges[360] -> front
    # ranges[180] -> right
    # ranges[540] -> left
    def scan_subscriber_handler(self, data):
        self.front_lidar_val = data.ranges[360]
        self.print("Front Lidar: " + str(data.ranges[360]))

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