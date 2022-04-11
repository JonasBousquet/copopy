import cv2
from matplotlib import pyplot as plt
import time

start = time.time()

# Path to hte images you want to compare
img1 = cv2.imread('./Frames/Eiffel/bild1.png')
img2 = cv2.imread('./Frames/Eiffel/bild3.jpeg')
# Initiate ORB detector
orb = cv2.ORB_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)


FLANN_INDEX_LSH = 6
index_params = dict(algorithm=FLANN_INDEX_LSH,
                   table_number=6, # 12
                   key_size=12,     # 20
                   multi_probe_level=1) #2
search_params = dict(checks=50)   # or pass empty dictionary

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1, des2, k=2)
matchesMask = [[0,0] for i in range(len(matches))]
count = 0


# ratio test as per Lowe's paper
for i, (m, n) in enumerate(matches):
    if m.distance < 0.7*n.distance:
        matchesMask[i] = [1, 0]
        count += 1

print('Used matches:', count)

draw_params = dict(matchColor=(0,255,0),
                   singlePointColor=(255,0,0),
                   matchesMask=matchesMask,
                   flags=0)

img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)

plt.imshow(img3,), plt.show()

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
