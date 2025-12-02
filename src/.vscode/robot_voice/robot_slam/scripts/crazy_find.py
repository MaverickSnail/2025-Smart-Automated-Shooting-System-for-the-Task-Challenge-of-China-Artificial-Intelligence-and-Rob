#!/usr/bin/env python

# coding: utf-8
"""
This is beautiful
This is wonderful
"""

import rospy
from geometry_msgs.msg import Point
import os
global find_id
find_id = None
recognize_flag = False

class object_position:
    def __init__(self):
        rospy.init_node("object_position", anonymous=True)
        self.ar_sub = rospy.Subscriber('/object_position', Point, self.find_cb) 
    
    def find_cb(self, data):
        global find_id, recognize_flag
        if recognize_flag:
            point_msg = data
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
                music_path = os.path.expanduser("~/music/target" + str(find_id) + ".mp3")
                os.system('mplayer %s' % music_path)

                recognize_flag = False  # Reset the flag after identification

if __name__ == '__main__':
    object_position_instance = object_position()
    rate = rospy.Rate(10)  # 10 Hz

    while not rospy.is_shutdown():
        print("If you want to find, please enter 1")
        try:
            a = int(input())
            if a == 1:
                recognize_flag = True
                # Wait for find_id to be updated
                while recognize_flag:
                    rate.sleep()
                print('target is ' + str(find_id))
        except ValueError:
            print("Please enter a valid integer.")
        rate.sleep()