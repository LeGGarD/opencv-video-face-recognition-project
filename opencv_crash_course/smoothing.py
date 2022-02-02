import cv2

image = cv2.imread('2.jpg')
cv2.imshow('Cat', image)
cv2.imwrite('for saving/cat2.jpg', image)

# average blur
average = cv2.blur(image, (3, 3))
cv2.imshow('Avg Blur', average)

# gaussian blur
gaussian = cv2.GaussianBlur(image, (7, 7), 0)
cv2.imshow('Gaussian', gaussian)
cv2.imwrite('for saving/gaussian_cat2.jpg', gaussian)

# median blur
median_blur = cv2.medianBlur(image, 7)
cv2.imshow('Median Blur', median_blur)
cv2.imwrite('for saving/median_cat2.jpg', median_blur)

# bilateral
bilateral = cv2.bilateralFilter(image, 11, 70, 70)
cv2.imshow('Bilateral', bilateral)
cv2.imwrite('for saving/bilateral_cat2.jpg', bilateral)

cv2.waitKey(0)