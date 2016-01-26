#!/usr/bin/env python

import rospy

from rospy_message_transporter.TCPServer import TCPServer
from rospy_message_transporter.JsonFormatter import JsonFormatter
from rospy_message_transporter.PublishingHandler import PublishingHandler

from dronemap_control.msg import RegistrationResponseMessage
from dronemap_control.msg import HeartbeatMessage

def create_message_formatter():
    msg_typ_attr_name = 'messageType'
    msg_typ_info = {}
    msg_typ_info['RegistrationResponseMessage'] = 'dronemap_control'
    msg_typ_info['HeartbeatMessage'] = 'dronemap_control'
    message_formatter = JsonFormatter(msg_typ_attr_name,msg_typ_info)
    return message_formatter

def create_message_handler():
    publishers_info = {}
    publishers_info['RegistrationResponseMessage'] = rospy.Publisher('registration', RegistrationResponseMessage, queue_size=10)
    publishers_info['HeartbeatMessage'] = rospy.Publisher('heartbeat', HeartbeatMessage, queue_size=10)
    message_handler = PublishingHandler(publishers_info)
    return message_handler

def launch_control_server_node():
    rospy.init_node('dronemap_control_server', anonymous=True)
    
    # get parameters for the server
    port_number = rospy.get_param('~port_number')
    buffer_size = rospy.get_param('~buffer_size')
    
    #get the formatter
    formatter = create_message_formatter()

    #get the handler
    handler = create_message_handler()

    #launch the server
    server = TCPServer("dronemap_control_server", port_number, formatter, handler, buffer_size)
    server.receive()

if __name__ == '__main__':
    try:
        launch_control_server_node()
    except :
        e = sys.exc_info()[0]
        t = e = sys.exc_info()[1]
        rospy.loginfo(rospy.get_caller_id() + "Error: %s" % e + ", Text: %s" % t)