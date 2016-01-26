import random
from dronemap_control.msg import RegistrationResponseMessage
from dronemap_control.msg import HeartbeatMessage
from rospy_message_transporter.Handler import Handler
from rospy_message_transporter.JsonFormatter import JsonFormatter

class SimulatedCloudServerHandler( Handler ):

    def __init__(self):
        self.message_formatter = JsonFormatter(None,{})

    def handle(self,ros_message, client_socket):
        if ros_message.messageType == 'RegistrationRequestMessage':
            response = RegistrationResponseMessage()
            response.status = int(random.getrandbits(1))
            response.messageType = 'RegistrationResponseMessage'
            if response.status == 1:
                print '...Registration accepeted'
                response.sessionID = 'SE123'
                response.UAVID = 'UAV123'
            else:
                print '...Registration refused'
            json_msg = self.message_formatter.format_from_ros_msg(response)
            client_socket.send(json_msg)
            print 'The sent reponse message is:' + json_msg
        elif ros_message.messageType == 'HeartbeatMessage':
            response = HeartbeatMessage()
            response.messageType = 'HeartbeatMessage'
            json_msg = self.message_formatter.format_from_ros_msg(response)
            client_socket.send(json_msg)
        #elif ros_message.messageType == 'MissionEndMessage'	
        