import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np

PI = np.pi
DANGER = 0.5
IDEAL = 0.75
MAX = 1.5
SPEED = 0.5
BACKUP = 0.25
NORM = PI / 2
FWD = PI
NORMSEARCH_MIN = 0
NORMSEARCH_MAX = PI * 1.5
TO_RAD = PI / 360.0
HOLD_WEIGHT = 0.3
FOLLOW_WEIGHT = 0.7

PUSH_CONST = IDEAL - DANGER
PULL_CONST = MAX - IDEAL

SEARCHMIN_I = int(NORMSEARCH_MIN / TO_RAD)
SEARCHMAX_I = int(NORMSEARCH_MAX / TO_RAD)

FPS = 10.0

class LabNode(Node):
  def __init__(self):
      super().__init__('lab_4_26_v2')

      self.scan_subscriber = self.create_subscription(LaserScan,'/scan',self.scan_subscriber_handler, 10)
      self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
      self.timer = self.create_timer(1.0/FPS, self.timer_callback)
  
  def timer_callback(self):
    if not self.ranges:
      return
    twist = Twist()
    twist.linear.x = SPEED
    twist.linear.y = twist.linear.z = 0.0
    twist.angular.z = 0.0
    twist.angular.x = twist.angular.y = 0.0
    casts = np.convolve(np.clip(self.ranges, 0.0, MAX), [0.2] * 5, mode = 'same')
    n_i = np.argmin(casts[SEARCHMIN_I : SEARCHMAX_I]) + SEARCHMIN_I
    c_i = np.argmin(casts)
    norm = casts[n_i], close = casts[c_i]
    if close <= DANGER:
      theta = c_i * TO_RAD
      direction = 1 if np.abs(theta - FWD) < PI / 2 else -1
      twist.linear.x = BACKUP * -direction
      twist.angular.z = (theta - FWD) * direction
      self.cmd_vel_publisher.publish(twist)
      return
    elif norm < MAX:
      theta = n_i * TO_RAD
      twist.linear.x = SPEED
      twist.angular.z = FOLLOW_WEIGHT * (theta - NORM) \
          + HOLD_WEIGHT * ( \
            ((norm - IDEAL) / PUSH_CONST) ** 2 if norm < IDEAL \
            else -((norm - IDEAL) / PULL_CONST) ** 2)
    if np.abs(c_i * TO_RAD - FWD) > PI / 2 and close < IDEAL:
      twist.angular.z += HOLD_WEIGHT * -((close - IDEAL) / PUSH_CONST) ** 2
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
