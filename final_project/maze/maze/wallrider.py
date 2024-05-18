import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np

# See writeup for full explanation.
# Note that for this, 0 degrees means behind, 90 means right, etc.

PI = np.pi                  # pi
DANGER = 0.1625             # unsafe wall radius (m)
IDEAL = 0.2                 # ideal wall following radius (m)
MAX = 0.48                  # max wall search radius (m)
SPEED = 0.5                 # normal speed (m/s)
BACKUP = 0.1                # slower speed for backing up / turning (m/s)
NORM = PI / 2               # direction of wall we should be following, e.g. right wall (rad)
FWD = PI                    # direction robot is going (180 degrees) (rad)
NORMSEARCH_MIN = PI * 0.25  # search between MIN and MAX for closest raycast on the right
NORMSEARCH_MAX = PI * 0.85 
FWDSEARCH_MIN = PI * 0.85   # search between MIN and MAX for closest raycast in front
FWDSEARCH_MAX = PI * 1.05
TO_RAD = PI / 360.0         # raycast array index to radians conversion factor
HOLD_WEIGHT = 1.0           # angular weighting to consider maintaining distance from wall
FOLLOW_WEIGHT = 2.0         # angular weighting to consider following the wall in the first place

# PRECALCULATIONS...
PUSH_CONST = (IDEAL - DANGER) * 0.75 # constant scaling factor for turning left if too close to wall
PULL_CONST = (MAX - IDEAL - 0.0025) * 0.375 # constant scaling factor for turning right if too far from wall

NORMSEARCHMIN_I = int(NORMSEARCH_MIN / TO_RAD) # indices of min/max search for right wall
NORMSEARCHMAX_I = int(NORMSEARCH_MAX / TO_RAD)
FWDSEARCHMIN_I = int(FWDSEARCH_MIN / TO_RAD) # indices of min/max search for forward wall
FWDSEARCHMAX_I = int(FWDSEARCH_MAX / TO_RAD)

FPS = 100.0 # number of times to publish per second

class LabNode(Node):
  def __init__(self):
      super().__init__('wallrider')
      self.get_logger().info("starting")
      # subscribe to lidar 
      self.scan_subscriber = self.create_subscription(LaserScan,'/scan',self.scan_subscriber_handler, 10)
      # publish to update cmd_vel
      self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
      self.timer = self.create_timer(1 / FPS, self.timer_callback)
  
  def timer_callback(self):
    # if we haven't gotten a raycast yet, don't calculate anything
    if not hasattr(self, "ranges"):
      return
    # create our twist object and default it to move forward
    twist = Twist()
    twist.linear.x = SPEED
    twist.linear.y = twist.linear.z = 0.0
    twist.angular.z = 0.0
    twist.angular.x = twist.angular.y = 0.0
    # clip raycasts while applying a convolution to average them out; e.g. sliding window average
    # this is to handle infs (by clipping them) and sharp values (by smoothing)
    A = np.clip(self.ranges, 0.0, MAX+0.1)
    casts = np.convolve(np.concatenate((A[-2:], A, A[:2])), [0.2] * 5, mode = 'valid')
    # use argmin to find the minimum's index (and not just the minimum)
    # this is to get the angle from it to do calculations
    # n_i / norm: index / distance from wall
    # f_i / fwd: index / distance from foward wall
    # c_i / norm: index / distance from closest object (in any direction)
    n_i = np.argmin(casts[NORMSEARCHMIN_I : NORMSEARCHMAX_I]) + NORMSEARCHMIN_I
    c_i = np.argmin(casts)
    f_i = np.argmin(casts[FWDSEARCHMIN_I : FWDSEARCHMAX_I]) + FWDSEARCHMIN_I
    norm = casts[n_i] # then get the actual distance from each
    close = casts[c_i]
    fwd = casts[f_i]
    if close <= DANGER: # if anything is in our danger zone
      theta = c_i * TO_RAD
      lin_dir = np.cos(theta) ** 3 # move in the opposite direction, 0 if on left/right
      ang_dir = np.sin(theta) # turn away if on the side, 0 if fwd/bkwd
      # move speed relative to BACKUP and our constants calculated earlier
      twist.linear.x = BACKUP * lin_dir
      twist.angular.z = ang_dir
      # publish and quit (do not consider anything else)
      self.cmd_vel_publisher.publish(twist)
      return
    # if there is some thing in front of us, turn left (past IDEAL to turn sooner)
    if fwd <= IDEAL + 0.6*(MAX - IDEAL):
      theta = f_i * TO_RAD # calculate angle of raycast
      twist.linear.x = BACKUP # use BACKUP speed
      # theta - NORM is the angular velocity we need to turn to make NORM on our right
      twist.angular.z = FOLLOW_WEIGHT * (theta - NORM)
      self.cmd_vel_publisher.publish(twist)
      return
    # if there is anything in view that is on our right, follow it
    if norm < MAX:
      theta = n_i * TO_RAD
      twist.linear.x = SPEED
      # scale angular velocity to turn it perp. from wall
      # plus quadratic scaling to maintain ideal distance from wall
      # quadratic -> scales more for objects far away from ideal
      twist.angular.z = FOLLOW_WEIGHT * (theta - NORM) \
          + HOLD_WEIGHT * ( \
            ((norm - IDEAL) / PUSH_CONST) ** 2 if norm < IDEAL \
            else -((norm - IDEAL) / PULL_CONST) ** 2)
    # if there is something on our left and within threatening distance, turn away from it
    # scale so that if turning is urgent, reduce linear speed
    twist.linear.x *= 1 - (2*twist.angular.z / PI) ** 2
    self.cmd_vel_publisher.publish(twist)
  
  # set our internal ranges whenever /scan gets a publish
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
