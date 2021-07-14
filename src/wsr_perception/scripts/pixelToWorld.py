#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import PointCloud2
import ros_numpy

def xyz(msg):
    # xyz_array = ros_numpy.point_cloud2.pointcloud2_to_xyz_array(msg)
    u = 200
    v = 100
    width = msg.width
    height = msg.height
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

def start_node():
    rospy.init_node('coordinate_extraction')
    rospy.loginfo('Coordinate extraction node started')
    rospy.Subscriber("camera/depth_registered/points",PointCloud2, xyz )
    rospy.spin()

if __name__ == '__main__':
    try: 
        start_node()
    except rospy.ROSInterruptException:
        pass