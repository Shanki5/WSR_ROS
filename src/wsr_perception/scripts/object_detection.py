#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

def showImage(img):
    cv2.imshow('image', img)
    cv2.waitKey(1)

def process_frame(msg):
    drawImg = 0
    try:
        bridge = CvBridge()
        orig = bridge.imgmsg_to_cv2(msg, "bgr8")
        drawImg = orig
        # Start coordinate, here (5, 5)
        # represents the top left corner of rectangle
        start_point = (200, 100)
        
        # Ending coordinate, here (220, 220)
        # represents the bottom right corner of rectangle
        end_point = (400, 300)
        
        # Blue color in BGR
        color = (255, 0, 0)
        
        # Line thickness of 2 px
        thickness = 2
        
        # Using cv2.rectangle() method
        # Draw a rectangle with blue line borders of thickness of 2 px
        drawImg = cv2.rectangle(drawImg, start_point, end_point, color, thickness)
    except Exception as err:
        print(err)
    showImage(drawImg)

def start_node():
    rospy.init_node('object_detection')
    rospy.loginfo('object detection node started')
    rospy.Subscriber("camera/rgb/image_color", Image, process_frame)
    rospy.spin()


if __name__ == '__main__':
    try: 
        start_node()
    except rospy.ROSInterruptException:
        pass