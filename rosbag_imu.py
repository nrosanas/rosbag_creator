import rosbag
import cv2
import rospy
from cv_bridge import CvBridge
from os import listdir
from sensor_msgs.msg import Imu

#VIDEO = "/home/noe/Projectes/esp32_capture/webcam.avi"
VIDEO = '/home/noe/Baixades/linear_accel_and_gyro_data_only-20211203T091829Z-001/linear_accel_and_gyro_data_only' \
        '/images/'
BAG = "aprilgrid.bag"
IMU = r"/home/noe/Baixades/linear_accel_and_gyro_data_only-20211203T091829Z-001/linear_accel_and_gyro_data_only" \
      r"/output_2021-12-03.txt"
freq = 20


bridge = CvBridge()
omega_x = omega_y = omega_z = alpha_x = alpha_y = alpha_z = 0
with rosbag.Bag(BAG, 'w') as bag, open(IMU) as file:
    for f in listdir(VIDEO):
        _, _, secs, nsecs, extension = f.split('.')
        frame = cv2.imread(VIDEO+f)

        stamp = rospy.rostime.Time(int(secs),int(nsecs))

        image_message = bridge.cv2_to_imgmsg(frame, encoding="passthrough")
        image_message.header.stamp = stamp
        image_message.header.frame_id = 'camera'
        bag.write("/camera/image_raw", image_message, stamp)
    for line in file.readlines():
        line.split()[1]
        if line.split()[1] == 'gyro':
            s_stamp, sensor, _, v0, v1, v2 = line.split()
            omega_x, omega_y, omega_z = v0[:-1], v1[:-1], v2
        elif line.split()[1] == 'accel':
            s_stamp, sensor, _, v0, v1, v2 = line.split()
            alpha_x, alpha_y, alpha_z = v0[:-1], v1[:-1], v2
        else:
            continue
        sec, nano = s_stamp[:-1].split('.')

        time = rospy.Time(int(sec), int(nano))
        imu_msg = Imu()
        imu_msg.header.stamp = time
        imu_msg.angular_velocity.x = float(omega_x)
        imu_msg.angular_velocity.y = float(omega_y)
        imu_msg.angular_velocity.z = float(omega_z)
        imu_msg.linear_acceleration.x = float(alpha_x)
        imu_msg.linear_acceleration.y = float(alpha_y)
        imu_msg.linear_acceleration.z = float(alpha_z)
        bag.write("/imu0", imu_msg, time)



