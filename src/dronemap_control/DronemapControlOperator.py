#!/usr/bin/env python
import sys
import rospy
from dronemap_control.msg import RegistrationRequestMessage
from dronemap_control.msg import RegistrationResponseMessage
from dronemap_control.msg import HeartbeatMessage
from dronemap_control.msg import MissionRequestMessage

class DronemapControlOperator( object ):

    def __init__(self, cloud_platform_client):
        self.cloud_client = cloud_platform_client
        
        rospy.loginfo(rospy.get_caller_id() + ": Prepare & send Registration Request")

        # Prepare a Registration Request message
        request = RegistrationRequestMessage()
        request.messageType = 'RegistrationRequestMessage'
        #get information from the status manager interface... implementation db or paramaeters or in-memory
        # information are 1-drone type
        # 2-battery level
        # 3- gps coords
        # 4 -serial number
        # s il te plais avant d implementet tout ca, test avec un simple example et verfier s interagit avec multiple callbacks
        
        # Send the Registration Request message & receive the Registration Response message
        response = self.cloud_client.send(request, True)

 
        if response == None or response.status == 0:
            rospy.loginfo(rospy.get_caller_id() + ": Registration Request refused")
            sys.exit() # Launch SystemExit exception, so it can be intercepted at an outler level
        

        rospy.set_param("/drone_registered", True)
        rospy.set_param("/cloud_session_id", response.sessionID)
        rospy.set_param("/cloud_drone_id", response.UAVID)

        rospy.loginfo(rospy.get_caller_id() + ": Registration Request accepted")
        # Store the received information to status manager

        
        
        # Start the Heartbeat message sending process
        # this process will start automatically by observing the server parameter variables.
        
        # Subscribe to topics
        #rospy.Subscriber('mission', MissionRequestMessage, self.missionRequestCallback)
        
        #rospy.Subscriber('heartbeat', HeartbeatMessage, self.HeartbeatCallback)
        #rospy.Subscriber('registration', RegistrationResponseMessage, self.registrationResponseCallback)


    def missionRequestCallback(data):
        rospy.loginfo(rospy.get_caller_id() + "Received Mission Request message %s", str(data))
    