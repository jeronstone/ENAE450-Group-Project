import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
 
lidar_alpha = 15
lidar_alpha_buffer = 0.01
distance_buffer = 0.1

class LabNode(Node):
    def __init__(self):
        super().__init__('lab_4_19')

        self.scan_subscriber = self.create_subscription(LaserScan,'/scan',self.scan_subscriber_handler,10)
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        self.declare_parameter('wall_dist', 0.3)
        self.distance = self.get_parameter('wall_dist').get_parameter_value().double_value
        self.declare_parameter('clockwise', True)
        self.clockwise = self.get_parameter('clockwise').get_parameter_value().bool_value
        self.front_lidar_val = None
        self.lidar_val = None
        self.lidar_alpha_diff = None
        self.turning = False
        self.init_travel = True

        self.turn_correction = True # true => dist ; false => ang
        self.turn_c = 0

        self.timer = self.create_timer(.1, self.timer_callback)
    
    def timer_callback(self):
        pose = Twist()

        if not self.turning:
            if not self.front_lidar_val or self.front_lidar_val > self.distance + 0.1:
                pose.linear.x = 0.1
            else:
                pose.linear.x = 0.0
                self.turning = True

            if not self.init_travel:
                # distance correction
                if self.turn_correction:
                    self.print("DISTANCE CORRECTION")
                    if self.distance - self.lidar_val > distance_buffer:
                        self.print("TOO CLOSE TO WALL: " + str(self.lidar_val))
                        if self.clockwise:
                            pose.angular.z = -0.2
                        else:
                            pose.angular.z = 0.2
                    elif self.distance - self.lidar_val < -distance_buffer:
                        self.print("TOO FAR FROM WALL: " + str(self.lidar_val))
                        if self.clockwise:
                            pose.angular.z = 0.2
                        else:
                            pose.angular.z = -0.2
                    else:
                        self.turn_correction = False
                        pose.angular.z = 0.0

                # ang correction
                else:
                    self.print("ANGLE CORRECTION; diff: " + str(self.lidar_alpha_diff))
                    if abs(self.lidar_alpha_diff) > lidar_alpha_buffer:
                        if self.lidar_alpha_diff > 0:
                            self.print("FACING OUTWARDS")
                            if self.clockwise:
                                pose.angular.z = 0.2
                            else:
                                pose.angular.z = -0.2
                        else:
                            self.print("FACING INWARDS")
                            if self.clockwise:
                                pose.angular.z = -0.2
                            else:
                                pose.angular.z = 0.2
                    else:
                        pose.angular.z = 0.0

        else:
            self.print("TURNING...")
            if self.turn_c < 30:
                if self.clockwise:
                    pose.angular.z = -(3.14/6.0)
                else:
                    pose.angular.z = (3.14/6.0)
                self.turn_c += 1
            else:
                pose.angular.z = 0.0
                self.turn_c = 0
                self.turning = False
                self.turn_correction = True
                self.init_travel = False
        
        self.cmd_vel_publisher.publish(pose)


    # ranges[0] -> back
    # ranges[360] -> front
    # ranges[180] -> right
    # ranges[540] -> left
    def scan_subscriber_handler(self, data):
        self.front_lidar_val = data.ranges[360]
        #self.print("Front Lidar: " + str(self.front_lidar_val))
        if self.clockwise:
            self.lidar_val = data.ranges[540]
            #self.print("Left Lidar: " + str(self.left_lidar_val))
                                       # upper                        # lower
            self.lidar_alpha_diff = data.ranges[540-lidar_alpha] - data.ranges[540+lidar_alpha]
        else:
            self.lidar_val = data.ranges[180]
                                        # upper                        # lower
            self.lidar_alpha_diff = data.ranges[180+lidar_alpha] - data.ranges[180-lidar_alpha]



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
