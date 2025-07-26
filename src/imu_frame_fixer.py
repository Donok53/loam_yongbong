#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Imu
from std_msgs.msg import Header

class ImuFrameFixer:
    def __init__(self):
        rospy.init_node('imu_frame_fixer', anonymous=True)
        
        # Subscribe to original IMU topic
        self.sub = rospy.Subscriber('/imu/data', Imu, self.imu_callback)
        
        # Publish to transformed IMU topic
        self.pub = rospy.Publisher('/imu/data_transformed', Imu, queue_size=10)
        
        # Simple noise filtering
        self.angular_velocity_threshold = 0.01  # rad/s
        self.linear_acceleration_threshold = 0.1  # m/s^2
        
        rospy.loginfo("IMU frame fixer started. Converting frame_id and filtering noise")
    
    def imu_callback(self, msg):
        # Create new IMU message with corrected frame_id and noise filtering
        new_msg = Imu()
        
        # Copy header with corrected frame_id
        new_msg.header = Header()
        new_msg.header.stamp = msg.header.stamp
        new_msg.header.frame_id = 'imu'
        
        # Copy orientation (quaternion)
        new_msg.orientation = msg.orientation
        new_msg.orientation_covariance = msg.orientation_covariance
        
        # Filter angular velocity noise
        new_msg.angular_velocity = msg.angular_velocity
        new_msg.angular_velocity.z = -msg.angular_velocity.z  # Fix z-axis sign
        
        # Apply noise threshold
        if abs(new_msg.angular_velocity.x) < self.angular_velocity_threshold:
            new_msg.angular_velocity.x = 0.0
        if abs(new_msg.angular_velocity.y) < self.angular_velocity_threshold:
            new_msg.angular_velocity.y = 0.0
        if abs(new_msg.angular_velocity.z) < self.angular_velocity_threshold:
            new_msg.angular_velocity.z = 0.0
            
        new_msg.angular_velocity_covariance = msg.angular_velocity_covariance
        
        # Filter linear acceleration noise
        new_msg.linear_acceleration = msg.linear_acceleration
        new_msg.linear_acceleration.z = -msg.linear_acceleration.z  # Fix z-axis sign
        
        # Apply noise threshold (except for z-axis which has gravity)
        if abs(new_msg.linear_acceleration.x) < self.linear_acceleration_threshold:
            new_msg.linear_acceleration.x = 0.0
        if abs(new_msg.linear_acceleration.y) < self.linear_acceleration_threshold:
            new_msg.linear_acceleration.y = 0.0
            
        new_msg.linear_acceleration_covariance = msg.linear_acceleration_covariance
        
        # Publish the corrected message
        self.pub.publish(new_msg)

if __name__ == '__main__':
    try:
        fixer = ImuFrameFixer()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass 