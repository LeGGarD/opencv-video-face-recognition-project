import cv2
import numpy as np

image = cv2.imread('1.jpg')
cv2.imshow('Cat', image)

blank = np.zeros(image.shape[:2], dtype='uint8')

mask = cv2.circle(blank.copy(), (image.shape[1]//2, image.shape[0]//2), 100, 255, -1)
cv2.imshow('Mask', mask)

rectangle = cv2.rectangle(blank.copy(), (30, 30), (370, 370), 255, -1)
cv2.imshow('Rectangle', rectangle)

weird_shape = cv2.bitwise_and(mask, rectangle)
cv2.imshow('weird_shape', weird_shape)

masked = cv2.bitwise_and(image, image, mask=weird_shape)
cv2.imshow('Masked Cat', masked)

cv2.waitKey(0)
