import rosbag
import cv2
import rospy
from cv_bridge import CvBridge

#VIDEO = "/home/noe/Projectes/esp32_capture/webcam.avi"
VIDEO = "/home/noe/Projectes/esp32_capture/table.avi"
BAG = "table2.bag"

freq = 20

cap = cv2.VideoCapture(VIDEO)

if not cap.isOpened():
    print("Error opening resource: " + str(VIDEO))
    print("Maybe opencv VideoCapture can't open it")
    exit(0)

bridge = CvBridge()
prop_fps = cap.get(cv2.CAP_PROP_FPS)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print("Info: Video height {} px".format(height))
if prop_fps != prop_fps or prop_fps <= 1e-2:
    print("Warning: can't get FPS. Assuming {}.".format(freq))
    prop_fps = freq
ret, frame = cap.read()

frame_id = 0
print(prop_fps)
with rosbag.Bag(BAG, 'w') as bag:
    while ret:
        ret, frame = cap.read()
        if ret:
            stamp = rospy.rostime.Time.from_sec(float(frame_id) / prop_fps)
            frame_id += 1
            image_message = bridge.cv2_to_imgmsg(frame, encoding="passthrough")
            image_message.header.stamp = stamp
            image_message.header.frame_id = 'camera'
            bag.write("/camera/image_raw", image_message, stamp)
        else:
            break
#cv2.destroyWindow("preview")
