# CALIBRATE CAMERAS STEREO FOR EVERY DAY

# 1) extract frames from video that I have synchronized by hand
# frames should be extracted at exact same time there is a sound based calibration function in opencv
# synchronisieren mit klopfen

import cv2
import time

start = time.time()

# Opens the Video file left
cap = cv2.VideoCapture('Vid/GP021230.MP4')
i = 0
print("camera r start")
while cap.isOpened():
    ret, frame = cap.read()
    if ret == False:
        break
    cv2.imwrite('./Frames/copo_L/copo_vid_L_' + str(i) + '.jpg', frame)
    i += 1
    if i == 500:
        break

print("camera r end")
cap.release()
cv2.destroyAllWindows()

# Opens the Video file right
capture = cv2.VideoCapture('Vid/GP021257.MP4')
i = 0
print("camera l start")
while capture.isOpened():
    ret, frame = capture.read()
    if ret == False:
        break
    cv2.imwrite('./Frames/copo_R/copo_vid_R_' + str(i) + '.jpg', frame)
    i += 1
    if i == 500:
        break
print("camera l end")
capture.release()
cv2.destroyAllWindows()

# Just  a timer to compare runtime (not necessary)
end = time.time()
zeit = end - start
if zeit > 60:
    minutes = int(zeit / 60)
    sec = zeit % 60
    sec = round(sec, 2)
    print(f'\nscript run in {minutes} m and {sec} s')
else:
    zeit = round(zeit, 2)
    print(f'\nscript run in {zeit} s')
