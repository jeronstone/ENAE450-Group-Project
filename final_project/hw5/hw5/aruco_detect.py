import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from interface_package.srv import ArucoDetectSrv
import cv2
from time import sleep

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()
#detector = cv2.aruco.ArucoDetector(dictionary, parameters)

class ArucoNode(Node):
    def __init__(self):
        super().__init__('aruco_detection_node')

        self.print('Initialized Node')
        self.scan_subscriber = self.create_subscription(Image,'/camera/image_raw/compressed',self.frame_handler,10)
        self.print('Created Subscriber to /camera/image_raw/compressed')
        #self.aruco_client = self.create_client(ArucoDetectSrv, '/aruco_detected')

    # Handles each camera frame
    def frame_handler(self, image_data):
        self.print("Got Frame {image_data.header.frame_id} @ {image_data.header.stamp}")

        # get camera frame data
        frame = image_data.data

        # detect arucos
        (corners, ids, rejected) = cv2.aruco.detectMarkers(frame)

        self.print("Detected: -----------")
        self.print(';;'.join(','.join(str(y) for y in x) for x in corners))
        self.print("IDs: ")
        self.print(';;'.join(str(x) for x in ids))
        self.print("---------------------")

        # if ids detected, publish to client
        # if len(ids) > 0:
        #     req = ArucoDetectSrv.Request()
        #     req.id = ids[0] # assume only 1 detected
        
        #     self.aruco_client.call_async(req)

        # draw aruco on frame
        aruco_frame = cv2.aruco.drawDetectedMarkers(frame, corners)
        
        # TODO will this work?
        # What we could do is create a publisher that publishes the frame and we can use rqt viewer
        cv2.imshow(aruco_frame) 
        sleep(10) # otherwise the imshow will not work since function is called for every new frame

    # logger print wrapper for debugging
    def print(self, str):
        self.get_logger().info(str)

def main(args=None):
    rclpy.init(args=args)

    labnode = ArucoNode()

    rclpy.spin(labnode)
    
    labnode.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()