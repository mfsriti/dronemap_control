#!/usr/bin/env python

import rospy
import sys
from rospy_message_transporter.TCPClient import TCPClient
from rospy_message_transporter.JsonFormatter import JsonFormatter
from dronemap_control.HeartbeatControlOperator import HeartbeatControlOperator
from dronemap_control.msg import HeartbeatMessage
from dronemap_control.msg import MissionRequestMessage

def create_message_formatter():
    msg_typ_attr_name = 'messageType'
    msg_typ_info = {}
    msg_typ_info['HeartbeatMessage'] = 'dronemap_control'
    message_formatter = JsonFormatter(msg_typ_attr_name,msg_typ_info)
    return message_formatter

def launch_heartbeat_operator_node():
    rospy.init_node('dronemap_heartbeat_operator', anonymous=True)
    
    # get parameters from the ros parameters server
    platform_ip_address = rospy.get_param('/cloud_platform_ip_address')
    platform_port_number = rospy.get_param('/cloud_platform_port_number')
    buffer_size = rospy.get_param('/buffer_size')

    rate = rospy.Rate(50)
    if not rospy.has_param("/drone_registered"):
        rospy.set_param("/drone_registered", False)

    while not rospy.get_param("/drone_registered"):
        rospy.loginfo(rospy.get_caller_id() + ": Still not registered yet.")
        rate.sleep()

    print "yes, registered"
    
    # get the formatter
    formatter = create_message_formatter()

    # start the operator
    client = TCPClient("dronemap_heartbeat_operator", platform_ip_address, platform_port_number, formatter, buffer_size)
    HeartbeatControlOperator(client)
    
    # Keep python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        launch_heartbeat_operator_node()
    except:
        e = sys.exc_info()[0]
        rospy.loginfo(rospy.get_caller_id() + "Error: %s" % e )