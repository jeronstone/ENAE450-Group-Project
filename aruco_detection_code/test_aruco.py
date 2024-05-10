import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from final_project_interface.srv import ArucoDetectSrv
import cv2
from time import sleep

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_1000)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

class TestNode(Node):
    def __init__(self):
        super().__init__('test_aruco_detection')

        # TODO update topic name I think
        self.scan_subscriber = self.create_subscription(Image,'/image_raw',self.frame_handler,10)
        self.aruco_client = self.create_client(ArucoDetectSrv, '/aruco_detected')

    # Handles each camera frame
    def frame_handler(image_data, self):
        self.print("Got Frame {image_data.header.frame_id} @ {image_data.header.stamp}")

        # get camera frame data
        frame = image_data.data

        # detect arucos
        (corners, ids, rejected) = detector.detectMarkers(frame)

        self.print("Detected: -----------")
        self.print(';;'.join(','.join(str(y) for y in x) for x in corners))
        self.print("IDs: ")
        self.print(';;'.join(str(x) for x in ids))
        self.print("---------------------")

        # if ids detected, publish to client
        if len(ids) > 0:
            req = ArucoDetectSrv.Request()
            req.corners = corners
            req.ids = ids
        
            self.aruco_client.call_async(req)

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

    labnode = TestNode()

    rclpy.spin(labnode)
    
    labnode.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()