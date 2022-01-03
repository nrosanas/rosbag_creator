import re

FILE = '/home/noe/Imatges/esp32/2021-11-08 IMU and ESP video timestamped/imu_data.txt'
with open(FILE) as f:
    i=0
    for lines in f.readlines():
        print(i)
        i+= 1
