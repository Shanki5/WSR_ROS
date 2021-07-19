#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import PointCloud2
from vision_msgs.msg import Detection2DArray
import ros_numpy

# global vars
received_detections = False
u = None
v = None

def detectionCB(msg):
    global u,v
    u, v, _ = msg.detections[0].bbox.center
    received_detections = True


def xyz(msg):
    # xyz_array = ros_numpy.point_cloud2.pointcloud2_to_xyz_array(msg)
    global u, v
    width = msg.width
    height = msg.height
    if(received_detections):
        point_step = msg.point_step
        row_step = msg.row_step

        array_pos = v*row_step + u*point_step

        bytesX = [ord(x) for x in msg.data[array_pos:array_pos+4]]
        bytesY = [ord(x) for x in msg.data[array_pos+4: array_pos+8]]
        bytesZ = [ord(x) for x in msg.data[array_pos+8:array_pos+12]]

        byte_format=struct.pack('4B', *bytesX)
        X = struct.unpack('f', byte_format)[0]

        byte_format=struct.pack('4B', *bytesY)
        Y = struct.unpack('f', byte_format)[0]

        byte_format=struct.pack('4B', *bytesZ)
        Z = struct.unpack('f', byte_format)[0]
        rospy.loginfo("X: %s",X)
        rospy.loginfo("Y: %s",Y)
        rospy.loginfo("Z: %s",Z)
        received_detections = False

def start_node():
    rospy.init_node('coordinate_extraction')
    rospy.loginfo('Coordinate extraction node started')
    rospy.Subscriber("camera/depth_registered/points",PointCloud2, xyz )
    rospy.Subscriber("/yolo_ros/detection", Detection2DArray, detectionCB)
    rospy.spin()

if __name__ == '__main__':
    try: 
        start_node()
    except rospy.ROSInterruptException:
        pass