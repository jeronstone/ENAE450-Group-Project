# ENAE450-Group-Project
For part 2 and 3, connect to a turtlebot, export the environmental variables in a second terminal,
and bringup the turtlebot in the first terminal. Then, in the second terminal, run:
colcon build --symlink-install
source install/setup.bash

Part 2: Turtbot: Inside wall following
Once in workspace, run this command in the second terminal:
ros2 launch lab_package lab_launch.py

Currently, the parameters are set so that the robot moves clockwise around the inside of the area
and stays a distance of 0.5 from the wall. Edit the parameters in the launch file to adjust.

Part 3: Turtbot: Outside wall following
Once in the workspace, run this command in the second terminal:
ros2 run lab_package lab_publish_vel_v2
