import rosbag
import cv2
import rospy
import time as t
from cv_bridge import CvBridge
from os import listdir

PATH = '/home/noe/Imatges/esp32/2021-11-10_demo_cube_2_480p_8fps-20211111T143726Z-001/2021-11-10_demo_cube_2_480p_8fps/'
IMU_DATA = '/home/noe/Imatges/esp32/2021-11-08 IMU and ESP video timestamped/imu_data.txt'

FILE_NAME = 'esp32_480.bag'
freq = 20

DOWN_SCALE = (640, 480)

with rosbag.Bag(FILE_NAME, 'w') as bag:
    for file in listdir(PATH):
        if file == 'imu_data.txt':
            pass
        else:
            seconds, nseconds, _ = file.split('.')
            time = rospy.Time(int(seconds), int(nseconds))
            im = cv2.imread(PATH + file, )
            im = cv2.resize(im, DOWN_SCALE, interpolation=cv2.INTER_LINEAR)
            bridge = CvBridge()
            image_message = bridge.cv2_to_imgmsg(im, encoding="passthrough")
            image_message.header.stamp = time
            bag.write("/cam0/image_raw", image_message, time)


IMU_DATA = '/home/noe/Imatges/esp32/2021-11-08 IMU and ESP video timestamped/imu_data.txt'
with open(IMU_DATA) as f:
    i=0
    for lines in f.readlines():
        print(i)
        i+= 1
