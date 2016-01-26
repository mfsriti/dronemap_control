cmake_minimum_required(VERSION 2.8.3)
project(dronemap_control)

find_package(catkin REQUIRED COMPONENTS
  message_generation
  rospy
  rostest
  std_msgs
  rospy_message_transporter
)

# Generate messages in the 'msg' folder
add_message_files(
  FILES
  GPSCoordinate.msg
  GPS.msg
  HeartbeatMessage.msg
  RegistrationRequestMessage.msg
  RegistrationResponseMessage.msg
  MissionRequestMessage.msg
)

catkin_python_setup()


generate_messages()

catkin_package(
  CATKIN_DEPENDS message_runtime std_msgs
)

# Test launch files
#add_rostest(test/test_all.test)