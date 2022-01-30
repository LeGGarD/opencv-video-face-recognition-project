import cv2

image = cv2.imread('2.jpg')
cv2.imshow('Cat', image)

# average blur
average = cv2.blur(image, (3, 3))
cv2.imshow('Avg Blur', average)

# gaussian blur
gaussian = cv2.GaussianBlur(image, (3, 3), 0)
cv2.imshow('Gaussian', gaussian)

# median blur
median_blur = cv2.medianBlur(image, 7)
cv2.imshow('Median Blur', median_blur)

# bilateral
bilateral = cv2.bilateralFilter(image, 11, 45, 45)
cv2.imshow('Bilateral', bilateral)

cv2.waitKey(0)