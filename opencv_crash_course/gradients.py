import cv2
import numpy as np

imgname = '5.jpg'
image = cv2.imread(imgname)
cv2.imshow('Cat', image)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray', gray)

# laplasian
lap = cv2.Laplacian(gray, cv2.CV_64F)
lap = np.uint8(np.absolute(lap))
cv2.imshow('Lap', lap)
# cv2.imwrite('for saving/zlata/asya_lap.jpg', lap)

# sobel
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
combined_sobel = cv2.bitwise_or(sobelx, sobely)

cv2.imshow('Sobel X', sobelx)
cv2.imshow('Sobel Y', sobely)
cv2.imshow('combined_sobel', combined_sobel)

# cv2.imwrite('for saving/zlata/asya_sobelx.jpg', sobelx)
# cv2.imwrite('for saving/zlata/asya_sobely.jpg', sobely)

canny = cv2.Canny(gray, 150, 175)
cv2.imshow('Canny', canny)

cv2.waitKey(0)