gnome-terminal --window -e 'bash -c "roscore; exec bash"'

gnome-terminal --tab -e 'bash -c "source ~/anaconda3/etc/profile.d/conda.sh && conda deactivate && exec bash --norc -c '\''sleep 3; source ~/RMIAB3/devel/setup.bash; roslaunch abot_bringup robot_with_imu.launch; exec bash'\''"' \
--tab -e 'bash -c "source ~/anaconda3/etc/profile.d/conda.sh && conda deactivate && exec bash --norc -c '\''sleep 3; source ~/RMIAB3/devel/setup.bash; roslaunch abot_bringup shoot.launch; exec bash'\''"' \
--tab -e 'bash -c "source ~/anaconda3/etc/profile.d/conda.sh && conda deactivate && exec bash --norc -c '\''sleep 4; source ~/RMIAB3/devel/setup.bash; roslaunch robot_slam navigation.launch; exec bash'\''"' \
--tab -e 'bash -c "source ~/anaconda3/etc/profile.d/conda.sh && conda deactivate && exec bash --norc -c '\''sleep 3; source ~/abot_vision/devel/setup.bash; roslaunch track_tag usb_cam_with_calibration.launch; exec bash'\''"' \
--tab -e 'bash -c "source ~/anaconda3/etc/profile.d/conda.sh && conda deactivate && exec bash --norc -c '\''sleep 3; source ~/abot_vision/devel/setup.bash; roslaunch track_tag ar_track_camera.launch; exec bash'\''"' \
--tab -e 'bash -c "source ~/anaconda3/etc/profile.d/conda.sh && conda deactivate && exec bash --norc -c '\''sleep 3; source ~/RMIAB3/devel/setup.bash; roslaunch find_object_2d find_object_2d.launch; exec bash'\''"'

gnome-terminal --tab -e 'bash -c "source ~/anaconda3/etc/profile.d/conda.sh && conda activate py38 && cd /home/abot/RMIAB3/src/robot_slam/scripts/ && source ~/3XRW7J/devel/setup.bash && rosrun robot_slam 2025_shoot_demo.py; exec bash"' \
--tab -e 'bash -c "source ~/anaconda3/etc/profile.d/conda.sh && conda activate py38 && sleep 4 && source ~/RMIAB3/devel/setup.bash && rosrun robot_slam 2025_shoot_target.py; exec bash"' \
--tab -e 'bash -c "source ~/anaconda3/etc/profile.d/conda.sh && conda activate py38 && sleep 3 && source ~/RMIAB3/devel/setup.bash && rosrun robot_slam 2025_yuyin_new.py; exec bash"'

gnome-terminal --tab -e 'bash -c "source ~/anaconda3/etc/profile.d/conda.sh && conda deactivate && exec bash --norc -c '\''sleep 15; source ~/RMIAB3/devel/setup.bash; roslaunch user_demo multi_goal_shoot.launch; exec bash'\''"'
