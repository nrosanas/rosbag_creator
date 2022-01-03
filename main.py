import rosbag
import cv2
import rospy
from sensor_msgs.msg import Imu
import pandas as pd
from cv_bridge import CvBridge


PATH = '/home/noe/Baixades/MN_050_HH_01/handheld0/'
freq = 20

img_df = pd.read_csv(PATH + 'cam0/data.csv')
imu_df = pd.read_csv(PATH + 'imu0/data.csv')
with rosbag.Bag('test.bag', 'w') as bag:
    for i, row in img_df.iterrows():
        time = rospy.Time(0, row['#timestamp [ns]'])
        file = row['filename']
        im = cv2.imread(PATH+'cam0/data/'+file,)
        bridge = CvBridge()
        image_message = bridge.cv2_to_imgmsg(im, encoding="passthrough")
        image_message.header.stamp = time
        bag.write("/cam0/image_raw", image_message, time)

    for j, row in imu_df.iterrows():
        time = rospy.Time(0, row['#timestamp [ns]'])
        imu_msg = Imu()
        imu_msg.header.stamp = time
        imu_msg.angular_velocity.x = row['w_RS_S_x [rad s^-1]']
        imu_msg.angular_velocity.y = row['w_RS_S_y [rad s^-1]']
        imu_msg.angular_velocity.z = row['w_RS_S_z [rad s^-1]']
        imu_msg.linear_acceleration.x = row['a_RS_S_x [m s^-2]']
        imu_msg.linear_acceleration.y = row['a_RS_S_y [m s^-2]']
        imu_msg.linear_acceleration.z = row['a_RS_S_z [m s^-2]']
        bag.write("/imu0", imu_msg, time)
