import cv2
import numpy as np
import os
import time
import datetime

from utils import CFEVideoConf, image_resize
import glob

# Video Input and Splitting
in_vid = cv2.VideoCapture('example.mp4')
img_dir = "Frames"
seconds_duration = 16
seconds_between_shots = .35

try:
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
except OSError:
    print('Error: Creating directory of frames')
now = datetime.datetime.now()
finish_time = now + datetime.timedelta(seconds=seconds_duration)
currentFrame = 0
frame_rate = 40
save_path = 'output.mp4'
config = CFEVideoConf(in_vid, filepath=save_path, res='720p')
out = cv2.VideoWriter(save_path, config.video_type, frame_rate, config.dims)
while datetime.datetime.now() < finish_time:
    ret, frame = in_vid.read()
    filename = f"{img_dir}/{currentFrame}.jpg"
    currentFrame += 1
    cv2.imwrite(filename, frame)
    time.sleep(seconds_between_shots)

# Combine images to Video
image_list = glob.glob(f"{img_dir}/*.jpg")
for file in image_list:
    image_frame = cv2.imread(file)
    image = image_resize(image_frame, width=config.width)
    out.write(image)

# All Release
in_vid.release()
out.release()
cv2.destroyAllWindows()
