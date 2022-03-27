import cv2
import matplotlib.pyplot as plt

img_name = '8.jpg'
savepath = 'for saving/' + 'zlata/'

image = cv2.imread(img_name)
cv2.imshow('Cat', image)

# BGR to Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('Cat Gray', gray)

# BGR to HueSaturationValue
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
cv2.imshow('Cat HSV', hsv)
cv2.imwrite(savepath + 'hsv' + img_name, hsv)

# BGR to LAB
lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
cv2.imshow('Cat LAB', lab)
cv2.imwrite(savepath + 'lab' + img_name, lab)

# BGR to LAB
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
cv2.imshow('Cat RGB', rgb)
cv2.imwrite(savepath + 'rgb' + img_name, rgb)

# plt.imshow(image)
# plt.show()

cv2.waitKey(0)