import cv2
import numpy as np

image = cv2.imread('1.jpg')

blank = np.zeros(image.shape, dtype='uint8')
cv2.imshow('Blank', blank)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('Cat Gray', gray)

blur = cv2.GaussianBlur(image, (5, 5), cv2.BORDER_DEFAULT)
cv2.imshow('Cat Blur', blur)

canny = cv2.Canny(blur, 100, 100)
cv2.imshow('Cat Canny', canny)

# canny_gray = cv2.Canny(gray, 100, 100)
# cv2.imshow('Cat Gray Canny', canny_gray)

ret, thresh = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY)
cv2.imshow('Thresh', thresh)

contours, hierarchies = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(len(contours))

cv2.drawContours(blank, contours, -1, (0, 0, 255), 1)
cv2.imshow('Contours', blank)

cv2.waitKey(0)