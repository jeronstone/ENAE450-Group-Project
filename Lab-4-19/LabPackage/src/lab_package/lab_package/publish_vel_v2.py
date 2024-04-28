import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np

PI = np.pi
DANGER = 0.175
IDEAL = 0.35
MAX = 0.6
SPEED = 0.5
BACKUP = 0.1
NORM = PI / 2
FWD = PI
NORMSEARCH_MIN = PI * 0.25
NORMSEARCH_MAX = PI * 0.9
FWDSEARCH_MIN = PI * 0.75
FWDSEARCH_MAX = PI * 1.25
TO_RAD = PI / 360.0
HOLD_WEIGHT = 2.0
FOLLOW_WEIGHT = 2.0

PUSH_CONST = IDEAL - DANGER
PULL_CONST = MAX - IDEAL

NORMSEARCHMIN_I = int(NORMSEARCH_MIN / TO_RAD)
NORMSEARCHMAX_I = int(NORMSEARCH_MAX / TO_RAD)
FWDSEARCHMIN_I = int(FWDSEARCH_MIN / TO_RAD)
FWDSEARCHMAX_I = int(FWDSEARCH_MAX / TO_RAD)

FPS = 10.0

class LabNode(Node):
  def __init__(self):
      super().__init__('lab_4_26_v2')

      self.scan_subscriber = self.create_subscription(LaserScan,'/scan',self.scan_subscriber_handler, 10)
      self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
      self.timer = self.create_timer(1.0/FPS, self.timer_callback)
  
  def timer_callback(self):
    if not hasattr(self, "ranges"):
      return
    twist = Twist()
    twist.linear.x = SPEED
    twist.linear.y = twist.linear.z = 0.0
    twist.angular.z = 0.0
    twist.angular.x = twist.angular.y = 0.0
    casts = np.convolve(np.clip(self.ranges, 0.0, MAX+0.5), [0.2] * 5, mode = 'same')
    n_i = np.argmin(casts[NORMSEARCHMIN_I : NORMSEARCHMAX_I]) + NORMSEARCHMIN_I
    f_i = np.argmin(casts[FWDSEARCHMIN_I : FWDSEARCHMAX_I]) + FWDSEARCHMIN_I
    c_i = np.argmin(casts)
    norm = casts[n_i]
    close = casts[c_i]
    fwd = casts[f_i]
    if close <= DANGER:
      self.get_logger().info("DANGER")
      theta = c_i * TO_RAD
      lin_dir = np.cos(theta)
      ang_dir = np.sin(theta)
      self.get_logger().info(f"{fwd} {f_i * TO_RAD}")
      twist.linear.x = BACKUP * lin_dir
      twist.angular.z = ang_dir
      self.get_logger().info(f"EEE{twist.linear.x} {twist.angular.z}")
      self.cmd_vel_publisher.publish(twist)
      return
    if fwd <= (IDEAL + MAX) / 2.0:
      self.get_logger().info("FWD TURN")
      theta = f_i * TO_RAD
      twist.linear.x = BACKUP
      twist.angular.z = FOLLOW_WEIGHT * (theta - NORM)
      self.cmd_vel_publisher.publish(twist)
      return
    if norm < MAX:
      self.get_logger().info("FOLLOWING NORM")
      theta = n_i * TO_RAD
      twist.linear.x = SPEED
      twist.angular.z = FOLLOW_WEIGHT * (theta - NORM) \
          + HOLD_WEIGHT * ( \
            ((norm - IDEAL) / PUSH_CONST) ** 2 if norm < IDEAL \
            else -((norm - IDEAL) / PULL_CONST) ** 2)
    if np.abs(c_i * TO_RAD - FWD) > PI / 2 and close < IDEAL:
      self.get_logger().info("LEFT IDEAL")
      twist.angular.z += HOLD_WEIGHT * -((close - IDEAL) / PUSH_CONST) ** 2
    self.get_logger().info(f"{twist.linear.x} {twist.angular.z}")
    twist.linear.x = 1 - (2*twist.angular.z / PI) ** 2
    self.cmd_vel_publisher.publish(twist)
      
  # ranges[0] -> back
  # ranges[360] -> front
  # ranges[180] -> right
  # ranges[540] -> left
  def scan_subscriber_handler(self, data):
      self.ranges = np.array(data.ranges)

def main(args=None):
  rclpy.init(args=args)
  labnode = LabNode()
  rclpy.spin(labnode)
  labnode.destroy_node()
  rclpy.shutdown()

if __name__ == '__main__':
  main()
