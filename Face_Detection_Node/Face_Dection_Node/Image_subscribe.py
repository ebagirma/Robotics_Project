#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError




# Callback for the Image message
def image_callback(img_msg):


    bridge = CvBridge()                             # Initialize the CvBridge class
    cv2.namedWindow("Face Detection", 1)            # Initialize an OpenCV Window

   
    #  Had Issues with Ros Melodic on getting haarcascade_frontalface_default.xml file 
    #  with the cv2 package so I have included it to this xml file with the relative path in
    face_detector = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')          


    # Try to convert the ROS Image message to a CV2 Image
    # Had Issues with ros melodic with python3 so done the testing with python2 and it work
    # If you run into this issue maybe try https://rancheng.github.io/ros-python2-3-conflict/
    try:
        cv_image = bridge.imgmsg_to_cv2(img_msg)
    except CvBridgeError:
        print("Error")
    

    # To make the display faster try I converted it to gray scale and then pass it to the face_detector. (for higher accuracy try the rgb image) 
    # Also, the scaleFactor is set to a 1.3 which is a higher downsamples factor. (for higher accuracy try lower value like 1.1y)
    # In additon (64, 64) the face size is higher, and doesn't seach for small faces. (to account for small faces try smaller values like (32,32))  
    gray_img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    face_rects = face_detector.detectMultiScale(gray_img, 1.3, 5, minSize=(64, 64))
    
    
    for (x, y, w, h) in face_rects:             # face bounding boxes 
        cv2.rectangle(img = gray_img,           # draw a rectangle around the face
                      pt1 = (x, y), 
                      pt2 = (x + w, y + h), 
                      color  =  (255, 255, 255), 
                      thickness = 3)          

    # Show the image with the bounding box
    cv2.imshow("Image Window", gray_img)
    cv2.waitKey(3)


def listener():
    rospy.init_node('Image Subscriber', anonymous=True)         # Initialize the ROS Node 
    print("About to start Image Subscriber")
    rospy.Subscriber("/camera", Image, image_callback)          # Initalize a subscriber to the with the camera

    while not rospy.is_shutdown():
        rospy.spin()

if __name__ == '__main__':
    listener()

