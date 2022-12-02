#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def talker():
    rospy.init_node('talker', anonymous=True)                       # Intialiaze the node
    # Define a publisher that will publish a message to a topic 'chatter'
    publisher = rospy.Publisher('/chatter', String, queue_size=10)     
   
    rate = rospy.Rate(10)                   # loop runs at 10hz or 0.1 seconds

    while not rospy.is_shutdown():          # loops until the node is shutdown
        # Define a string data type          
        # Assign a value to the string                                                                                                       
        hello_str = "hello world it is %s" % rospy.get_time()  
        # Publish the message        
        publisher.publish(hello_str)        
        rate.sleep()                        

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass