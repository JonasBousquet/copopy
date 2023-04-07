import cv2
import numpy as np

# load stereo camera parameters
stereo_params = cv2.FileStorage('stereo_params.xml', cv2.FILE_STORAGE_READ)
cam_mats, cam_dist = [], []
for i in range(2):
    cam_mats.append(stereo_params.getNode('cameraMatrix{}'.format(i)).mat())
    cam_dist.append(stereo_params.getNode('distCoeffs{}'.format(i)).mat())
R = stereo_params.getNode('R').mat()
T = stereo_params.getNode('T').mat()

# read MP4 files
cap_left = cv2.VideoCapture('left.mp4')
cap_right = cv2.VideoCapture('right.mp4')

while cap_left.isOpened() and cap_right.isOpened():
    # read left and right frames
    ret1, frame1 = cap_left.read()
    ret2, frame2 = cap_right.read()

    if not ret1 or not ret2:
        break

    # rectify images
    R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(cam_mats[0], cam_dist[0],
                                                       cam_mats[1], cam_dist[1],
                                                       frame1.shape[:2][::-1], R, T)
    map1_x, map1_y = cv2.initUndistortRectifyMap(cam_mats[0], cam_dist[0], R1, P1,
                                                  frame1.shape[:2][::-1], cv2.CV_32FC1)

    map2_x, map2_y = cv2.initUndistortRectifyMap(cam_mats[1], cam_dist[1], R2, P2,
                                                  frame1.shape[:2][::-1], cv2.CV_32FC1)

    frame1_rect = cv2.remap(frame1, map1_x, map1_y, cv2.INTER_LINEAR)
    frame2_rect = cv2.remap(frame2, map2_x, map2_y, cv2.INTER_LINEAR)

    # compute disparity map
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    disparity_map = stereo.compute(cv2.cvtColor(frame1_rect, cv2.COLOR_BGR2GRAY),
                                    cv2.cvtColor(frame2_rect, cv2.COLOR_BGR2GRAY))

    # compute depth map
    depth_map = cv2.reprojectImageTo3D(disparity_map, Q)

    # map 2D coordinates to 3D coordinates
    # left_x, left_y, right_x, right_y are the 2D coordinates in the left and right images
    left_x, left_y = 100, 200
    right_x, right_y = 80, 200

    disparity = disparity_map[left_y, left_x]
    z_coord = depth_map[left_y, left_x][2]
    focal_length = cam_mats[0][0][0]
    baseline = np.linalg.norm(T)
    x_coord = (left_x - (cam_mats[0][0][2] - cam_mats[1][0][2])) * z_coord / focal_length
    y_coord = (left_y - cam_mats[0][1][2]) * z_coord / focal_length

    print("Object 3D coordinates: ({}, {}, {})".format(x_coord, y_coord, z_coord))

    cv2.imshow('Left', frame1_rect)
    cv2.imshow('Right', frame2_rect)

    if cv2.waitKey(1) == ord('q'):
        break

cap_left.release()
cap_right.release()
cv2.destroyAllWindows()
