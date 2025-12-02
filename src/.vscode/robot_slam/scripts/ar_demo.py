#!/usr/bin/env python

#coding: utf-8

import rospy
from ar_track_alvar_msgs.msg import AlvarMarkers

id = 0

class ArTracker:
    def __init__(self):
        rospy.init_node('ar_tracker_node',anonymous=True)
        self.ar_sub = rospy.Subscriber('/ar_pose_marker', AlvarMarkers, self.ar_cb)

    def ar_cb(self, data):
        global id
        for marker in data.markers:
            id = marker.id
            print(id)

if __name__ == '__main__':
    try:
        ar_tracker = ArTracker()
        rospy.spin()
    except rospy.ROSInterruptExcepyton:
        pass