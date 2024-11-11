import cv2
import numpy as np
import matplotlib.pyplot as plt

def emtpy_callback(_):
    pass


cap = cv2.VideoCapture(0)
cv2.namedWindow('Filtros')
# cv2.namedWindow('Original')
# cv2.namedWindow('Mask')
# cv2.namedWindow('Filtered')
# cv2.namedWindow('Blobs')
cv2.resizeWindow('Filtros', 640, 480)
# cv2.resizeWindow('Original', 640, 480)
# cv2.resizeWindow('Mask', 640, 480)
# cv2.resizeWindow('Filtered', 640, 480)
# cv2.resizeWindow('Blobs', 640, 480)




cv2.createTrackbar("LH", "Filtros", 0, 179, emtpy_callback)
cv2.createTrackbar("LS", "Filtros", 0, 255, emtpy_callback)
cv2.createTrackbar("LV", "Filtros", 0, 255, emtpy_callback)
cv2.createTrackbar("UH", "Filtros", 179, 179, emtpy_callback)
cv2.createTrackbar("US", "Filtros", 255, 255, emtpy_callback)
cv2.createTrackbar("UV", "Filtros", 255, 255, emtpy_callback)
cv2.setTrackbarPos("LH", "Filtros", 102)
cv2.setTrackbarPos("LS", "Filtros", 122)
cv2.setTrackbarPos("LV", "Filtros", 44)
cv2.setTrackbarPos("UH", "Filtros", 123)


params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = 1000
params.maxArea = 1000000
params.filterByCircularity = False
params.filterByConvexity = False
params.filterByInertia = False
detector = cv2.SimpleBlobDetector_create(params)


while True:
    ret, frame = cap.read()
    if not ret:
        break
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    lh = cv2.getTrackbarPos("LH", "Filtros")
    ls = cv2.getTrackbarPos("LS", "Filtros")
    lv = cv2.getTrackbarPos("LV", "Filtros")
    uh = cv2.getTrackbarPos("UH", "Filtros")
    us = cv2.getTrackbarPos("US", "Filtros")
    uv = cv2.getTrackbarPos("UV", "Filtros")


    lower = np.array([lh, ls, lv])
    upper = np.array([uh, us, uv])
    mask = cv2.inRange(hsv, lower, upper)


    res = cv2.bitwise_and(frame, frame, mask=mask)
    inverted_mask = cv2.bitwise_not(mask)
    keypoints = detector.detect(inverted_mask)
    frame_with_keypoints = cv2.drawKeypoints(res, keypoints, np.array([]), (0, 255, 255),
                                             cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


    frame = cv2.resize(frame, (640, 280))
    mask = cv2.resize(mask, (640, 280))
    res = cv2.resize(res, (640, 280))
    inverted_mask = cv2.resize(inverted_mask, (640, 280))
    frame_with_keypoints = cv2.resize(frame_with_keypoints, (640, 280))
    # cv2.imshow("Original", frame)
    # cv2.imshow("Mask", mask)
    # cv2.imshow("Filtered Output", res)
    # cv2.imshow("Blobs", inverted_mask)
    cv2.imshow("Filtros", frame_with_keypoints)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


    # plot_histograms(hsv)


cap.release()
cv2.destroyAllWindows()
