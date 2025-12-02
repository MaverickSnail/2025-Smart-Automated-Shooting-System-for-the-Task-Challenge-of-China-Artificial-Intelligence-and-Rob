#!/usr/bin/env python

#coding: utf-8
"""
Do not use any Chinese!!!
"""

import rospy

import actionlib
from actionlib_msgs.msg import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf_conversions import transformations
from math import pi
from std_msgs.msg import String

from ar_track_alvar_msgs.msg import AlvarMarkers
from ar_track_alvar_msgs.msg import AlvarMarker

from geometry_msgs.msg import Point
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os

class NavigationDemo:
    def __init__(self):
        self.set_pose_pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=5)
        self.arrive_pub = rospy.Publisher('/voiceWords', String, queue_size=10)
        self.ar_sub = rospy.Subscriber('/object_position', Point, self.find_cb)
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        self.move_base.wait_for_server(rospy.Duration(60))
        self.find_id = 1  # Default value to ensure it's within 1-8 range
        self.recognize_flag = False

    def find_cb(self, data):
        point_msg = data
        if self.recognize_flag:
            if point_msg.z != 255:
                if 10 <= point_msg.z <= 19:
                    self.find_id = 1
                elif 20 <= point_msg.z <= 29:
                    self.find_id = 2
                elif 30 <= point_msg.z <= 39:
                    self.find_id = 3
                elif 40 <= point_msg.z <= 49:
                    self.find_id = 4
                elif 50 <= point_msg.z <= 59:
                    self.find_id = 5
                elif 60 <= point_msg.z <= 69:
                    self.find_id = 6
                elif 70 <= point_msg.z <= 79:
                    self.find_id = 7
                elif 80 <= point_msg.z <= 89:
                    self.find_id = 8
                
                print(point_msg)
                print('target is ' + str(self.find_id))
                target_path = "~/music/" + 'target' + str(self.find_id) + ".mp3"
                os.system('mplayer %s' % target_path)
                self.recognize_flag = False
    
    def get_find_id(self):
        return self.find_id

    def set_pose(self, p):
        if self.move_base is None:
            return False
        x, y, th = p
        pose = PoseWithCovarianceStamped()
        pose.header.stamp = rospy.Time.now()
        pose.header.frame_id = 'map'
        pose.pose.pose.position.x = x
        pose.pose.pose.position.y = y
        q = transformations.quaternion_from_euler(0.0, 0.0, th / 180.0 * pi)
        pose.pose.pose.orientation.x = q[0]
        pose.pose.pose.orientation.y = q[1]
        pose.pose.pose.orientation.z = q[2]
        pose.pose.pose.orientation.w = q[3]

        self.set_pose_pub.publish(pose)
        return True

    def _done_cb(self, status, result):
        rospy.loginfo("navigation done! status:%d result:%s" % (status, result))
        arrive_str = "arrived to target point"
        self.arrive_pub.publish(arrive_str)

    def _active_cb(self):
        rospy.loginfo("[Navi] navigation has been activated")

    def _feedback_cb(self, feedback):
        msg = feedback
        # rospy.loginfo("[Navi] navigation feedback\r\n%s"%feedback)

    def goto(self, p):
        rospy.loginfo("[Navi] goto %s" % p)
        # arrive_str = "going to next point"
        # self.arrive_pub.publish(arrive_str)
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = p[0]
        goal.target_pose.pose.position.y = p[1]
        q = transformations.quaternion_from_euler(0.0, 0.0, p[2] / 180.0 * pi)
        goal.target_pose.pose.orientation.x = q[0]
        goal.target_pose.pose.orientation.y = q[1]
        goal.target_pose.pose.orientation.z = q[2]
        goal.target_pose.pose.orientation.w = q[3]

        self.move_base.send_goal(goal, done_cb=self._done_cb, active_cb=self._active_cb, feedback_cb=self._feedback_cb)
        finished_within_time = self.move_base.wait_for_result(rospy.Duration(300))  # 5 minutes timeout

        if not finished_within_time:
            self.move_base.cancel_goal()
            rospy.loginfo("Timed out achieving goal")
        else:
            state = self.move_base.get_state()
            if state == GoalStatus.SUCCEEDED:
                rospy.loginfo("Goal succeeded!")
            else:
                rospy.loginfo("Goal failed with error code: " + str(state))

    def run(self):
        rospy.loginfo("Starting navigation demo")
        # Here you can set the initial pose or other setup tasks
        self.set_pose([0.0, 0.0, 0.0])

        # Example of how to use the goto function
        waypoints = [
            [1.0, 1.0, 90.0],
            [2.0, 2.0, 180.0],
            [3.0, 3.0, 270.0]
        ]

        for waypoint in waypoints:
            rospy.loginfo("Navigating to waypoint: %s" % waypoint)
            self.goto(waypoint)
            rospy.sleep(1)  # Sleep to simulate waiting between waypoints

if __name__ == '__main__':
    rospy.init_node('navigation_demo', anonymous=True)
    demo = NavigationDemo()
    demo.run()
    rospy.spin()
