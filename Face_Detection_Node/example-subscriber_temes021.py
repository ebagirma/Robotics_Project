#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from tf2_msgs.msg import TFMessage
from sensor_msgs.msg import Imu


#******************************** The callbacks for each topic *********************************
def callback_chatter(data):                             
    rospy.loginfo("/CHATTER - str: %s", data.data)     

def callback_tf(transforms):                            
    x = transforms.transforms[0].transform.translation.x
    w = transforms.transforms[0].transform.rotation.w
    rospy.loginfo("/TF -- translation x: %s rotation w: %s ", x, w)  

def callback_imu(imu):
    rospy.loginfo("/IMU - acceleration x: %s", imu.linear_acceleration.x)    
     
#************************************* End of callbacks *****************************************
     
def listener():
    # Intialize the listener node
    rospy.init_node('listener', anonymous=True)
    # 1. listens to the /imu topic
    rospy.Subscriber("/imu", Imu, callback_imu)
    # 2. listens to the /chatter topic
    rospy.Subscriber("/chatter", String, callback = callback_chatter)
    # 3. listens to the /tf topic
    rospy.Subscriber("/tf", TFMessage,  callback_tf)
    # continue listing until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()