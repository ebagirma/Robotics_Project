import random                                       # To Generate random number
import rospy
from geometry_msgs.msg import Twist                 # To move the robot
from sensor_msgs.msg import LaserScan               # if obstacle is present then we want to sense it



def myhook():                       # Set the robot to stop before shuting down
    move_random=  Twist()
    move_random.linear.x = 0.0
    move_random.linear.y = 0.0
    move_random.linear.z = 0.0
    move_random.angular.x = 0.0
    move_random.angular.y = 0.0
    move_random.angular.z = 0.0
    pub.publish(move_random)
    print("shutdown time!") 



#******************************** Tyies to Dance while Avoid Obstacle *********************************
"""
In case the turtubot is a world where there are obstacle,
like turtublebot3_world we want to avoid obstacle

"""

def callback(laser):

    print ('-------------------------------------------')
    
    threshold = 1 # Laser scan range threshold
    random_velocity_linear_x = random.randint(-5, 5)
    random_velocity_angualr_z = random.randint(-5, 5)

    print('Random Value Generated for linear velocity x is ', random_velocity_linear_x)
    print('Random Value Generated for linear angular z is  ', random_velocity_angualr_z)

    if laser.ranges[0]>threshold and laser.ranges[15]>threshold and laser.ranges[345]>threshold:            # No obstacle infront
        # Checks if there are obstacles in front and 15 degrees left and right 

        if random_velocity_linear_x > 0:                # Randomly Moving forward and rotating
            move_random.linear.x  = random_velocity_linear_x
            move_random.angular.z =  random_velocity_angualr_z                             
        else:                                           # If random value of x is negative we don't know if we have obstacle behind or not so,    
            move_random.linear.x  = 0                              # Stop moving forward
            move_random.angular.z = random_velocity_angualr_z      # Rotate
            
    else:                                               # May be obstacle in front 
        if random_velocity_linear_x > 0:                         # If we get positive linear velocity x
            move_random.linear.x = 0.0                                 # stop
            move_random.angular.z = random_velocity_angualr_z          # rotate 
        else:                                                    # If we get negative linear velocity x
            move_random.linear.x  = random_velocity_linear_x           # move backward
            move_random.angular.z =  0                                 # Do not rotate (angular velocity)

        if laser.ranges[0]>threshold and laser.ranges[15]>threshold and laser.ranges[345]>threshold:
            move_random.linear.x = random_velocity_linear_x
            move_random.angular.z = 0.0

    print ('-------------------------------------------')
    pub.publish(move_random)                              # publish the move object

#************************************End of Callback*******************************************




if __name__=="__main__":
    rospy.init_node('trying_to_avoidance_obestacle')                # Initializes the node
    rate = rospy.Rate(10) 

    try:
        while not rospy.is_shutdown():
            
            move_random = Twist()                                           # Creates a Twist message type object
            pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)         # Publisher to "/cmd_vel" topic                                                
            sub = rospy.Subscriber("/scan", LaserScan, callback)            # Subscriber the "/scan" Topic from LaserScan

            rospy.on_shutdown(myhook)                                       # Avoid spinning after shutdown
            rospy.spin()                                                    
                        
    except:
        print("error")



