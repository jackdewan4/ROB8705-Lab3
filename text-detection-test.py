# import the necessary packages
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import numpy as np
import cv2

import random as rng

rng.seed(12345)


def thresh_callback(val):
    threshold = val
    
    canny_output = cv2.Canny(grayOutput, threshold, threshold * 2)
    
    
    contours, _ = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    
    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)
    centers = [None]*len(contours)
    radius = [None]*len(contours)
    for i, c in enumerate(contours):
        contours_poly[i] = cv2.approxPolyDP(c, 3, True)
        boundRect[i] = cv2.boundingRect(contours_poly[i])
        # centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])
    
    
    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    
    
    for i in range(len(contours)):
        color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        # cv2.drawContours(drawing, contours_poly, i, color)
        cv2.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
          (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
        # cv2.circle(drawing, (int(centers[i][0]), int(centers[i][1])), int(radius[i]), color, 2)
    
    
    cv2.imshow('Contours', drawing)
    cv2.imwrite('contours.png', drawing)
# define the dictionary of digit segments so we can identify
# each digit on the license plate
DIGITS_LOOKUP = {
	(1, 1, 1, 0, 1, 1, 1): 0,
	(0, 0, 1, 0, 0, 1, 0): 1,
	(1, 0, 1, 1, 1, 1, 0): 2,
	(1, 0, 1, 1, 0, 1, 1): 3,
	(0, 1, 1, 1, 0, 1, 0): 4,
	(1, 1, 0, 1, 0, 1, 1): 5,
	(1, 1, 0, 1, 1, 1, 1): 6,
	(1, 0, 1, 0, 0, 1, 0): 7,
	(1, 1, 1, 1, 1, 1, 1): 8,
	(1, 1, 1, 1, 0, 1, 1): 9
}

# load the example image
image = cv2.imread("sweetwhip.jpg")
# pre-process the image by resizing it, converting it to
# graycale, blurring it, and computing an edge map
image = imutils.resize(image, height=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 50, 200, 255)
cv2.imshow("Input", image)
cv2.imshow("edged", edged)
# find contours in the edge map, then sort them by their
# size in descending order
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)



cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
displayCnt = None
# loop over the contours
for c in cnts:
	# approximate the contour
	perimeter = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
	# if the contour has four vertices, then we have found
	# the thermostat display
	if len(approx) == 4:
		displayCnt = approx
		break
	
# extract the thermostat display, apply a perspective transform
# to it
warped = four_point_transform(gray, displayCnt.reshape(4, 2))
output = four_point_transform(image, displayCnt.reshape(4, 2))

grayOutput = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
# threshold the warped image, then apply a series of morphological
# operations to cleanup the thresholded image
thresh = cv2.threshold(warped, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cv2.imshow('thresh', thresh)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
# thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# cv2.imshow('threshMorph', thresh)


# src_gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
# src_gray = cv2.blur(thresh, (3,3))
source_window = 'Source'
cv2.namedWindow(source_window)
cv2.imshow(source_window, thresh)
max_thresh = 255
init_thresh = 150 # initial threshold
cv2.createTrackbar('Canny thresh:', source_window, init_thresh, max_thresh, thresh_callback)
thresh_callback(init_thresh)
# find contours in the thresholded image, then initialize the
# digit contours lists
# cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
# 	cv2.CHAIN_APPROX_SIMPLE)
# cnts = imutils.grab_contours(cnts)
# digitCnts = []
# # loop over the digit area candidates
# for count, c in enumerate(cnts):
# 	# compute the bounding box of the contour
# 	(x, y, w, h) = cv2.boundingRect(c)

# 	# print('width', w)
# 	# print('contour: ', count)
	
# 	# taking out the contour conditions to draw bounding box around all contours found
# 	# # if the contour is sufficiently large, it must be a digit
# 	# if w >= 15 and (h >= 15 and h <= 60):
# 	# 	digitCnts.append(c)
# 	digitCnts.append(c)
# # sort the contours from left-to-right, then initialize the
# # actual digits themselves
# print('digitCnts: ', digitCnts)
# digitCnts = contours.sort_contours(digitCnts,
# 	method="left-to-right")[0]
# digits = []

# print('digiCnts sorted: ', digitCnts)


# # taking the digit check out since the segments wont align with this digit font


# # # loop over each of the digits
# for c in digitCnts:
# 	# extract the digit ROI
# 	(x, y, w, h) = cv2.boundingRect(c)
# 	roi = thresh[y:y + h, x:x + w]
# 	# compute the width and height of each of the 7 segments
# 	# we are going to examine
# 	(roiH, roiW) = roi.shape
# 	(dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
# 	dHC = int(roiH * 0.05)
# # 	# define the set of 7 segments
# 	segments = [
# 		((0, 0), (w, dH)),	# top
# 		((0, 0), (dW, h // 2)),	# top-left
# 		((w - dW, 0), (w, h // 2)),	# top-right
# 		((0, (h // 2) - dHC) , (w, (h // 2) + dHC)), # center
# 		((0, h // 2), (dW, h)),	# bottom-left
# 		((w - dW, h // 2), (w, h)),	# bottom-right
# 		((0, h - dH), (w, h))	# bottom
# 	]
# 	on = [0] * len(segments)
	

# # loop over the segments
# # for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
# #     # extract the segment ROI, count the total number of
# #     # thresholded pixels in the segment, and then compute
# #     # the area of the segment
# #     segROI = roi[yA:yB, xA:xB]
# #     total = cv2.countNonZero(segROI)
# #     area = (xB - xA) * (yB - yA)
# #     # if the total number of non-zero pixels is greater than
# #     # 50% of the area, mark the segment as "on"
# #     if total / float(area) > 0.5:
# #         on[i]= 1
# # # lookup the digit and draw it on the image
# # digit = DIGITS_LOOKUP[tuple(on)]
# # digits.append(digit)
# cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 1)
# # cv2.putText(output, str(digit), (x - 10, y - 10),
# # cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)

# # display the digits
# # print(u"{}{}.{} \u00b0C".format(*digits))
cv2.imshow("Input", image)
cv2.imshow("Output", output)
cv2.waitKey(0)

