import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_1000)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

class TestNode(Node):
    def __init__(self):
        super().__init__('test_aruco_detection')

        # TODO update topic name I think
        self.scan_subscriber = self.create_subscription(Image,'/image_raw',self.frame_handler,10)

    # Handles each camera frame
    def frame_handler(image_data, self):
        self.print("Got Frame {image_data.header.frame_id} @ {image_data.header.stamp}")

        # get camera frame data
        frame = image_data.data

        # detect arucos
        (corners, ids, rejected) = detector.detectMarkers(frame)

        self.print("Detected: -----------")
        self.print(' '.join(str(x) for x in corners))
        self.print("IDs: ")
        self.print(' '.join(str(x) for x in ids))
        self.print("---------------------")

        # draw aruco on frame
        aruco_frame = cv2.aruco.drawDetectedMarkers(frame, corners)
        
        # TODO will this work?
        cv2.imshow(aruco_frame) 

    # logger print wrapper for debugging
    def print(self, str):
        self.get_logger().info(str)

def main(args=None):
    rclpy.init(args=args)

    labnode = TestNode()

    rclpy.spin(labnode)
    
    labnode.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()