#!/usr/bin/env python

import rospy
import sys
from rospy_message_transporter.TCPClient import TCPClient
from rospy_message_transporter.JsonFormatter import JsonFormatter
from dronemap_control.DronemapControlOperator import DronemapControlOperator
from dronemap_control.msg import RegistrationResponseMessage
from dronemap_control.msg import MissionRequestMessage

def create_message_formatter():
    msg_typ_attr_name = 'messageType'
    msg_typ_info = {}
    msg_typ_info['RegistrationResponseMessage'] = 'dronemap_control'
    msg_typ_info['MissionRequestMessage'] = 'dronemap_control'
    message_formatter = JsonFormatter(msg_typ_attr_name,msg_typ_info)
    return message_formatter

def launch_control_operator_node():
    rospy.init_node('dronemap_control_operator', anonymous=True)
    
    # get parameters for the client
    platform_ip_address = rospy.get_param('~cloud_platform_ip_address')
    platform_port_number = rospy.get_param('~cloud_platform_port_number')
    buffer_size = rospy.get_param('~buffer_size')

    # set global parameters for other processes (eg. hearbeat_operator_node)
    rospy.set_param('/cloud_platform_ip_address', platform_ip_address)
    rospy.set_param('/cloud_platform_port_number', platform_port_number)
    rospy.set_param('/buffer_size', buffer_size)
    
    rospy.set_param('/drone_registered', False)
    
    
    # get the formatter
    formatter = create_message_formatter()

    # start the operator
    client = TCPClient("dronemap_control_operator", platform_ip_address, platform_port_number, formatter, buffer_size)
    DronemapControlOperator(client)
    
    # Keep python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        launch_control_operator_node()
    except:
        e = sys.exc_info()[0]
        rospy.loginfo(rospy.get_caller_id() + "Error: %s" % e )