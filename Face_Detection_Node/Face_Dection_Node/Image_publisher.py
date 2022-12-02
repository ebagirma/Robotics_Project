#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


def publish_Image():

  rospy.init_node('Publisher', anonymous=True)              # Inialize node
  pub = rospy.Publisher('camera', Image, queue_size=10)     # Publish camera topic
  

  rate = rospy.Rate(10)                  # Go through the loop 10 times per second
  webcam = cv2.VideoCapture(0)           # Get the default webcam.

  
  cv_bridge = CvBridge()                  # Used to convert between ROS and OpenCV images


  while not rospy.is_shutdown():

      ret, frame = webcam.read()          # Capture each frames from the camera
      if ret == True:           
        rospy.loginfo('Image being Published')
        pub.publish(cv_bridge.cv2_to_imgmsg(frame))         # Convert image to a ROS image message

      rate.sleep()              # Sleep with the defined rate

if __name__ == '__main__':
  try:
    publish_Image()
  except rospy.ROSInterruptException:
    pass