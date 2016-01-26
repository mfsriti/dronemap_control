#!/usr/bin/env python
import sys
import rospy

from dronemap_control.msg import HeartbeatMessage

class HeartbeatControlOperator( object ):

    def __init__(self, cloud_platform_client):
        self.cloud_client = cloud_platform_client
        
        # Prepare a Heartbeat message

        rate = rospy.Rate(0.3) # 3 seconds?
       
        while not rospy.is_shutdown() and rospy.get_param("/drone_registered"):
            rospy.loginfo(rospy.get_caller_id() + ": Send Heartbeat message.")
            heartbeat = HeartbeatMessage()
            heartbeat.sessionID =  rospy.get_param("/cloud_session_id")
            heartbeat.droneID =  rospy.get_param("/cloud_drone_id")

            heartbeat.messageType = "HeartbeatMessage"
            try :
                 self.cloud_client.send(heartbeat)
            except :
                e = sys.exc_info()[0]
                t = e = sys.exc_info()[1]
                rospy.loginfo(rospy.get_caller_id() + "Error: %s" % e + ", Text: %s" % t)
            rate.sleep()

      