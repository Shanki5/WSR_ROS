#!/usr/bin/env python
import rospy

#lets assume that ros is publishing a msg containing X,Y,Z in terms of the robots's base frame


from geometry_msgs.msg import Point
from std_msgs.msg import Float64MultiArray
from math import atan2,sqrt,sin,cos, pi
from sensor_msgs.msg import JointState
from std_msgs.msg import Header



# node initialization
rospy.init_node('controller', anonymous=True)
pub = rospy.Publisher('joint_steps',Float64MultiArray, queue_size=10)
pub2 = rospy.Publisher('joint_states',JointState, queue_size=10)

#robot physical constants 
Al = 177
Au = 180
L2 = 71 
Lo = 41 
L1o = 40
Zo = -77

rad2deg = 180.0/pi
deg2rad = pi/180.0
gearRatio = 5.1
rad2deggeared = rad2deg*gearRatio 
deg2radgeared = deg2rad*gearRatio

base_offset = 0.0
shoulder_offset = deg2rad * 142.0
elbow_offset = deg2rad * 45.0

def calc_joint_angles(x, y, z):
    theta1 = atan2(y,x)
    x = x - cos(theta1)*L1o
    y = y - sin(theta1)*L1o
    z = z - Zo - L2


    L1 = sqrt(x*x + y*y) - Lo
    L7 = sqrt(L1*L1 + z*z)

    a = z/L7
    b = (L7*L7 + Al*Al - Au*Au)/(2*L7*Al)
    c = (Al*Al + Au*Au - L7*L7)/(2*Al*Au)

    theta2 = (atan2(a, sqrt(1 - a*a)) + atan2(sqrt(1 - b*b),b))

    theta3 = atan2(sqrt(1 - c*c),c)

    rospy.loginfo("Joint 1: %s",theta1)
    rospy.loginfo("Joint 2: %s", theta2)
    rospy.loginfo("joint 3: %s", theta3)

    theta1 = (theta1*rad2deggeared) - base_offset
    theta2 = theta2 - elbow_offset
    theta3 = theta3 - shoulder_offset
    theta3 = -((theta2 + theta3 ) * rad2deggeared)
    theta2 = theta2*rad2deggeared
    return theta1,theta2,theta3

def check_limit(theta1,theta2,theta3):
    pass

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data)
    theta1, theta2, theta3 = calc_joint_angles(data.x, data.y, data.z)
    # pub.publish(data=[theta1, theta2, theta3])
    hello_str = JointState()
    hello_str.header = Header()
    hello_str.header.stamp = rospy.Time.now()
    hello_str.name = ['Joint1', 'Joint2', 'Joint3']
    hello_str.position = [theta1/rad2deggeared, -theta2/rad2deggeared  , -(theta3 - theta2)/rad2deggeared]
    hello_str.velocity = []
    hello_str.effort = []
    pub2.publish(hello_str)
    


    
def listener():
    rospy.Subscriber("Target_Point", Point, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()



if __name__ == '__main__':
    listener()

