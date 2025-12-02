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
from nav_msgs.msg import Odometry
from geometry_msgs.msg  import Point
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os

id = 255
flog0 = 255
flog1 = 255
flog2 = 255
count = 0
move_flog = 0
global find_id
find_id = None
global recognize_flag
recognize_flag = False  # Initialize recognize_flag

class navigation_demo:
    def __init__(self):
        self.set_pose_pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=5)
        self.arrive_pub = rospy.Publisher('/voiceWords',String,queue_size=10)
        self.ob_sub = rospy.Subscriber('/object_position', Point, self.find_cb)
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        self.move_base.wait_for_server(rospy.Duration(60))
        self.ar_sub = rospy.Subscriber('/ar_pose_marker', AlvarMarkers, self.ar_cb)
        self.coord_sub = rospy.Subscriber('/odom',Odometry,self.callback)


    def ar_cb(self, data):
        global find_id, recognize_flag
        if recognize_flag == True:
            for marker in data.markers:
                find_id = marker.id
                music_path = "~/music/"+'target' + str(find_id) +".mp3" 
                os.system('mplayer %s' %music_path)
                recognize_flag = False
 
    def callback(self, data):

        position = data.pose.pose.position
        print(position.x, position.y)

    def find_cb(self, data):
        global find_id, recognize_flag
        point_msg = data
        if recognize_flag:
            if point_msg.z != 255:
                if 10 <= point_msg.z <= 19:
                    find_id = 1
                elif 20 <= point_msg.z <= 29:
                    find_id = 2
                elif 30 <= point_msg.z <= 39:
                    find_id = 3
                elif 40 <= point_msg.z <= 49:
                    find_id = 4
                elif 50 <= point_msg.z <= 59:
                    find_id = 5
                elif 60 <= point_msg.z <= 69:
                    find_id = 6
                elif 70 <= point_msg.z <= 79:
                    find_id = 7
                elif 80 <= point_msg.z <= 89:
                    find_id = 8
                print(point_msg)
                print('target is ' + str(find_id))
                target_path = "~/music/"+'target' + str(find_id) +".mp3" 
                os.system('mplayer %s' %target_path)
                recognize_flag = False

    def set_pose(self, p):
        if self.move_base is None:
            return False
        x, y, th = p
        pose = PoseWithCovarianceStamped()
        pose.header.stamp = rospy.Time.now()
        pose.header.frame_id = 'map'
        pose.pose.pose.position.x = x
        pose.pose.pose.position.y = y
        q = transformations.quaternion_from_euler(0.0, 0.0, th/180.0*pi)
        pose.pose.pose.orientation.x = q[0]
        pose.pose.pose.orientation.y = q[1]
        pose.pose.pose.orientation.z = q[2]
        pose.pose.pose.orientation.w = q[3]

        self.set_pose_pub.publish(pose)
        return True

    def _done_cb(self, status, result):
        rospy.loginfo("navigation done! status:%d result:%s"%(status, result))
        arrive_str = "arrived to traget point"
        # self.arrive_pub.publish(arrive_str)

    def _active_cb(self):
        rospy.loginfo("[Navi] navigation has be actived")

    def _feedback_cb(self, feedback):
        msg = feedback
        #rospy.loginfo("[Navi] navigation feedback\r\n%s"%feedback)
    def goto(self, p):
        rospy.loginfo("[Navi] goto %s" % p)
        rospy.loginfo(p)
        # arrive_str = "going to next point"
        # self.arrive_pub.publish(arrive_str)
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = p[0]
        goal.target_pose.pose.position.y = p[1]
        q = transformations.quaternion_from_euler(0.0, 0.0, p[2]/180.0*pi)
        goal.target_pose.pose.orientation.x = q[0]
        goal.target_pose.pose.orientation.y = q[1]
        goal.target_pose.pose.orientation.z = q[2]
        goal.target_pose.pose.orientation.w = q[3]

        self.move_base.send_goal(goal, self._done_cb, self._active_cb, self._feedback_cb)
        result = self.move_base.wait_for_result(rospy.Duration(60))
        if not result:
            self.move_base.cancel_goal()
            rospy.loginfo("Timed out achieving goal")
        else:
            state = self.move_base.get_state()
            if state == GoalStatus.SUCCEEDED:
                rospy.loginfo("reach goal %s succeeded!" % p)
        return True

    def cancel(self):
        self.move_base.cancel_all_goals()
        return True

    def arrive_announce(self, id):
        arrive_path = "~/music/" + 'arrive' + str(id) + ".mp3"
        os.system('mplayer %s' % arrive_path)


if __name__ == "__main__":
    rospy.init_node('navigation_demo', anonymous=True)
    goalListX = rospy.get_param('~goalListX')
    goalListY = rospy.get_param('~goalListY')
    goalListYaw = rospy.get_param('~goalListYaw')

    goals = [[float(x), float(y), float(yaw)] for (x, y, yaw) in zip(goalListX.split(","), goalListY.split(","), goalListYaw.split(","))]
    print(goals)
    print('Please press 1 to continue: ')
    input = raw_input()
    r = rospy.Rate(1)
    r.sleep()
    navi = navigation_demo()

    if input == '1':

     navi.goto(goals[1])
     rospy.sleep(6)
     navi.goto(goals[2])
     rospy.sleep(60)
     navi.goto(goals[3])
     rospy.sleep(60)
     navi.goto(goals[4])
     rospy.sleep(60)
     navi.goto(goals[5])
     rospy.sleep(60)
     navi.goto(goals[6])
     rospy.sleep(60)
     navi.goto(goals[7])
     rospy.sleep(60)
     navi.goto(goals[8])
     rospy.sleep(60)