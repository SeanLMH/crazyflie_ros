#!/usr/bin/env python

import rospy
import tf
from crazyflie_driver.msg import Motor
from std_msgs.msg import Empty
from crazyflie_driver.srv import UpdateParams

if __name__ == '__main__':
    rospy.init_node('motor', anonymous=True)

    rate = rospy.Rate(100) # 10 hz
    name = "cmd_motor"

    msg = Motor()
    msg.header.seq = 0
    msg.header.stamp = rospy.Time.now()
    msg.m1 = 0
    msg.m2 = 0
    msg.m3 = 0
    msg.m4 = 0

    pub = rospy.Publisher(name, Motor, queue_size=1)

    stop_pub = rospy.Publisher("cmd_stop", Empty, queue_size=1)
    stop_msg = Empty()

    rospy.wait_for_service('update_params')
    rospy.loginfo("found update_params service")
    update_params = rospy.ServiceProxy('update_params', UpdateParams)

    rospy.set_param("kalman/resetEstimation", 1)
    update_params(["kalman/resetEstimation"])
    rospy.sleep(0.1)
    rospy.set_param("kalman/resetEstimation", 0)
    update_params(["kalman/resetEstimation"])
    rospy.sleep(0.5)

    # take off
    while not rospy.is_shutdown():
        for y in range(10000):
            msg.m1 = y
            msg.m2 = y
            msg.m3 = y
            msg.m4 = y
            now = rospy.get_time()
            msg.header.seq += 1
            msg.header.stamp = rospy.Time.now()
            pub.publish(msg)
            rate.sleep()
        break

    stop_pub.publish(stop_msg)
