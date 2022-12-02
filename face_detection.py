
"""Publish a video as ROS messages.
"""



import numpy as np
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()

def main():

    # Set up node.
    rospy.init_node("video_publisher", anonymous=True)

    img_pub = rospy.Publisher("/image_raw", Image,
                              queue_size=10)

    # Open video.
    # video = cv2.VideoCapture(0)

    # # Get frame rate.
    # fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
    # rate = rospy.Rate(fps)

    # height = 400
    # width = 400
    video = cv2.VideoCapture(0)
    width  = int(video.get(3))
    height = int(video.get(4))
    fps = int(video.get(5))
    # Loop through video frames.
    while not rospy.is_shutdown() and video.grab():
        tmp, img = video.retrieve()

        if not tmp:
            print ("Could not grab frame.")
            break

        img_out = np.empty((height, width, img.shape[2]))

        # Compute input/output aspect ratios.
        aspect_ratio_in = np.float(img.shape[1]) / np.float(img.shape[0])
        aspect_ratio_out = np.float(width) / np.float(height)

        if aspect_ratio_in > aspect_ratio_out:
            # Output is narrower than input -> crop left/right.
            rsz_factor = np.float(height) / np.float(img.shape[0])
            img_rsz = cv2.resize(img, (0, 0), fx=rsz_factor, fy=rsz_factor,
                                 interpolation=cv2.INTER_AREA)

            diff = (img_rsz.shape[1] - width) / 2
            img_out = img_rsz[:, diff:-diff-1, :]
        elif aspect_ratio_in < aspect_ratio_out:
            # Output is wider than input -> crop top/bottom.
            rsz_factor = np.float(width) / np.float(img.shape[1])
            img_rsz = cv2.resize(img, (0, 0), fx=rsz_factor, fy=rsz_factor,
                                 interpolation=cv2.INTER_AREA)

            diff = (img_rsz.shape[0] - height) / 2

            img_out = img_rsz[diff:-diff-1, :, :]
        else:
            # Resize image.
            img_out = cv2.resize(img, (height, width))

        assert img_out.shape[0:2] == (height, width)

        try:
            # Publish image.
            img_msg = bridge.cv2_to_imgmsg(img_out, "bgr8")
            img_msg.header.stamp = rospy.Time.now()
            img_pub.publish(img_msg)


        except CvBridgeError as err:
            print(err)

        rate.sleep()

    return

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass