#!/usr/bin/env python
# -*- coding:  utf-8 -*-
import rospy
import math
import actionlib
import serial
import time
from std_msgs.msg import String
from actionlib_msgs.msg import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseWithCovarianceStamped,Point,Twist
from tf_conversions import transformations
from math import pi
import os
from ar_track_alvar_msgs.msg import AlvarMarkers
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
serialPort = "/dev/shoot"
baudRate = 9600
ser = serial.Serial(port = serialPort, baudrate = baudRate, parity = "N", bytesize = 8, stopbits = 1)

case = None
#Yaw_th = 0.0045
Yaw_th = 0.0042
Min_y = -0.43
Max_y = -0.37

class navigation_demo:
	def __init__(self):
		self.set_pose_pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size = 5)
		self.arrive_pub = rospy.Publisher('/voiceWords', String, queue_size = 10)
		self.find_sub = rospy.Subscriber('/object_position', Point, self.find_cb)
		self.ar_sub = rospy.Subscriber('/ar_pose_marker', AlvarMarkers, self.ar_cb)
		self.armove_sub = rospy.Subscriber('/ar_pose_marker', AlvarMarkers,self.armove_cb)
		#self.actmove_sub = rospy.Subscriber('/ar_pose_marker', String,self.act_move)
		self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
		self.move_base.wait_for_server(rospy.Duration(60))
		self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1000)
	def end(self):
		global time
		msg = Twist()
		msg.linear.x = -0.3
		msg.linear.y = -0.3
		msg.linear.z = 0.0
		msg.angular.x = 0.0
		msg.angular.y = 0.0
		msg.angular.z = 0.0
		while time <=15:
			self.pub.publish(msg)
			rospy.sleep(0.1)
			time += 1


	def ar_cb(self, data):
		global msg, ar_x_0_abs, ar_x_0, ar_y_0, Min_y, Max_y, Yaw_th, case
		ar_markers = data
		for marker in data.markers:
			if marker.id == 1 and case == 2:
			#if marker.id == 3 and case == 2:
				ar_x_0 = marker.pose.pose.position.x
				ar_y_0 = marker.pose.pose.position.y
				ar_x_0_abs = abs(ar_x_0)
				if ar_x_0_abs >= Yaw_th:
					msg = Twist()
					#msg.angular.z = -4.5 * ar_x_0
                                        msg.angular.z = -4.8 * ar_x_0
					self.pub.publish(msg)
					print("ar_x_0_abs:", ar_x_0_abs)
					print("ar_y_0:", ar_y_0)
				elif ar_y_0 <= Max_y and ar_y_0 >= Min_y and ar_x_0_abs < Yaw_th:
					ser.write(b'\x55\x01\x12\x00\x00\x00\x01\x69')
					print("shoot")
					#time.sleep(0.1)
					#time.sleep(0.04)
					time.sleep(0.05)
					ser.write(b'\x55\x01\x11\x00\x00\x00\x01\x68')
					rospy.sleep(1)
					case = 3
					msg = Twist()
					#msg.linear.x = -0.2671
					#msg.linear.y = -0.1168
					msg.linear.x = -0.29
					msg.linear.y = -0.116
					self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
					rate = rospy.Rate(10)
					start_time = rospy.Time.now()
					print(case)
					while (rospy.Time.now() - start_time).to_sec() < 4.0:
						self.pub.publish(msg)
						rate.sleep()
					msg.linear.x = 0
					msg.linear.y = 0
					self.pub.publish(msg)
					self.goto(goals[2])
					rospy.sleep(1)
					case = 4




	def armove_cb(self, data):
		global ar_x, ar_x_abs, Yaw_th, case
		move_markers = data
		for marker in data.markers:
			if marker.id == 7 and case == 4:
				ar_x = marker.pose.pose.position.x
				ar_x_abs = abs(ar_x)
#				if ar_x_abs <= Yaw_th:
#					ser.write(b'\x55\x01\x12\x00\x00\x00\x01\x69')
#					print("shoot")
#					time.sleep(0.1)
#					ser.write(b'\x55\x01\x11\x00\x00\x00\x01\x68')
#					rospy.sleep(2)
#					case = 5
#					self.goto(goals[3])
#					rospy.sleep(2)


				if ar_x_abs >= Yaw_th:
					msg = Twist()
					#msg.angular.z = -4.5 * ar_x
					msg.angular.z = -4.4 * ar_x
					self.pub.publish(msg)
					print(ar_x_abs)
				elif ar_x_abs < Yaw_th:
					ser.write(b'\x55\x01\x12\x00\x00\x00\x01\x69')
					print("shoot")
					#time.sleep(0.1)
					#time.sleep(0.08)
					time.sleep(0.05)
					ser.write(b'\x55\x01\x11\x00\x00\x00\x01\x68')
					rospy.sleep(1)
					case = 5
					self.goto(goals[3])
					rospy.sleep(1)
					case = 6
					print(case)
					q = transformations.quaternion_from_euler(0.0, 0.0, 0.0)
					msg = Twist()

					#msg.linear.x = -0.29
					#msg.linear.x = -0.158
					msg.linear.x = -0.15
					msg.linear.y = -0.09

					#msg.linear.x = -0.26733
					#msg.linear.y = -0.11694

					rate = rospy.Rate(1000)
					start_time = rospy.Time.now()
					print(case)
					while (rospy.Time.now() - start_time).to_sec() < 3.5:
						self.pub.publish(msg)

						rate.sleep()
					msg.linear.x = 0
					msg.linear.y = 0
					self.pub.publish(msg)
					case = 7
					
#	def act_move(self):
#		global case
#		if case == 6:
#			print(case)
#			q = transformations.quaternion_from_euler(0.0, 0.0, 0.0)
#			msg = Twist()
#			msg.linear.x = -0.220
#			msg.linear.y = -0.062
#			self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
#			rospy.Rate(10)
#			start_time = rospy.Time.now()
#			print(case)
#			while (rospy.Time.now() - start_time).to_sec() < 5.0:
#				self.pub.publish(msg)
#				rate.sleep()
#			msg.linear.x = 0
#			msg.linear.y = 0
#			self.pub.publish(msg)
#			case = 7
		


	def find_cb(self, data):
		global flog0, flog1, case
		point_msg = data
		#flog0 = point_msg.x - 320
		flog0 = point_msg.x - 319
		flog1 = abs(flog0)
		if flog1 > 10 and case == 0:
			#ser.write(b'\x55\x01\x12\x00\x00\x00\x01\x69')
			#print("shoot")
			#time.sleep(0.1)
			#time.sleep(0.05)
			#ser.write(b'\x55\x01\x11\x00\x00\x00\x01\x68')
			#rospy.sleep(2)
			msg = Twist()
			msg.angular.z = -0.018 * flog0
			#msg.angular.z = -0.013 * flog0
			self.pub.publish(msg)
			print(flog1)
		elif flog1 <= 10 and case == 0:
			ser.write(b'\x55\x01\x12\x00\x00\x00\x01\x69')
			print("shoot")
			#time.sleep(0.1)
			#time.sleep(0.08)
			time.sleep(0.06)
			ser.write(b'\x55\x01\x11\x00\x00\x00\x01\x68')
			rospy.sleep(1)
			case = 1
			msg = Twist()
			#msg.linear.x = -0.2671
			#msg.linear.y = -0.1168
			msg.linear.x = -0.3
			msg.linear.y = -0.116
			rate = rospy.Rate(10)
			start_time = rospy.Time.now()
			print(case)
			while (rospy.Time.now() - start_time).to_sec() < 4.0:
				self.pub.publish(msg)
				rate.sleep()
			msg.linear.x = 0
			msg.linear.y = 0
			self.pub.publish(msg)
			self.goto(goals[1])
			rospy.sleep(1)
			case = 2
			#case = 12		

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
		rospy.loginfo("navigation done! status:%d result:%s"%(status, result))
		arrive_str = "arrived to target point"
		self.arrive_pub.publish(arrive_str)
	def _active_cb(self):
		rospy.loginfo("[Navi] navigation has be actived")
	def _feedback_cb(self, feedback):
		msg = feedback
	def goto(self, p):
		rospy.loginfo("[Navi] goto %s"%p)
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
		self.move_base.send_goal(goal, self._done_cb, self._active_cb, self._feedback_cb)
		result = self.move_base.wait_for_result(rospy.Duration(60))
		if not result:
			self.move_base.cancel_goal()
			rospy.loginfo("Timed out achieving goal")
		else:
			state = self.move_base.get_state()
			if state == GoalStatus.SUCCEEDED:
			#if state - GoalStatus.SUCCEEDED < [0.05,0.05,0.01]:
				rospy.loginfo("reach goal %s succeeded!"%p)
		return True
	def cancel(self):
		self.move_base.cancel_all_goals()
		return True

if __name__ == "__main__":
	rospy.init_node('navigation_demo', anonymous = True)
	goalListX = rospy.get_param('~goalListX', '1.0,1.0,1.0')
	goalListY = rospy.get_param('~goalListY', '1.0,1.0,1.0')
	goalListYaw = rospy.get_param('~goalListYaw', '0.0,0.0,0.0')
	goals = [[float(x), float(y), float(yam)] for (x, y, yam) in zip(goalListX.split(","),goalListY.split(","),goalListYaw.split(","))]
	print('press 1 to continue:')
	input = raw_input()
	r = rospy.Rate(1)
	r.sleep()
	navi = navigation_demo()
	navi.goto(goals[0])
	rospy.sleep(2)
	case = 0


#	case = 4
#	if case == 6:
#		navi.act_move()
		
		


	while not rospy.is_shutdown():
		r.sleep()
