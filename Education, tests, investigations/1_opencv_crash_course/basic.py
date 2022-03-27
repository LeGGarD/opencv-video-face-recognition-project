import cv2

image = cv2.imread('1.jpg')
cv2.imshow('Cat', image)

# convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('Cat Grayscale', gray)

# blur
blur = cv2.GaussianBlur(image, (11, 11), cv2.BORDER_DEFAULT)
cv2.imshow('Blured Cat', blur)

# edge cascade
canny = cv2.Canny(blur, 100, 100)
cv2.imshow('Canny', canny)

# dilating the image
dilated = cv2.dilate(canny, (7, 7), iterations=3)
cv2.imshow('Dilated', dilated)

# Eroding
eroded = cv2.erode(dilated, (7, 7), iterations=3)
cv2.imshow('Eroded', eroded)

# resize
resized = cv2.resize(image, (image.shape[1]*2, image.shape[0]*2), interpolation=cv2.INTER_CUBIC)
cv2.imshow('Pappa', resized)

# cropping
cropped = image[100:200, 100:200]
cv2.imshow('Cropped', cropped)

cv2.waitKey(0)
