import cv2
import matplotlib.pyplot as plt

image = cv2.imread('1.jpg')
cv2.imshow('Cat', image)

# BGR to Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('Cat Gray', gray)

# BGR to HueSaturationValue
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
cv2.imshow('Cat HSV', hsv)

# BGR to LAB
lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
cv2.imshow('Cat LAB', lab)

# BGR to LAB
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
cv2.imshow('Cat RGB', rgb)

# plt.imshow(image)
# plt.show()

cv2.waitKey(0)