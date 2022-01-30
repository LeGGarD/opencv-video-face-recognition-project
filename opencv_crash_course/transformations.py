import cv2
import numpy as np

image = cv2.imread('1.jpg')
cv2.imshow('Cat', image)


# translating the image
def translate(img, x, y):
    trans_matrix = np.float32([[1, 0, x], [0, 1, y]])
    dimensions = (img.shape[1], img.shape[0])
    return cv2.warpAffine(img, trans_matrix, dimensions)


translated = translate(image, 100, -100)
cv2.imshow('Translated', translated)


# rotating
def rotate(img, angle, rot_point=None):
    (height, width) = img.shape[:2]

    if rot_point is None:
        rot_point = (width // 2, height // 2)

    rot_matrix = cv2.getRotationMatrix2D(rot_point, angle, 1.0)
    dimensions = (width, height)

    return cv2.warpAffine(img, rot_matrix, dimensions)

rotated = rotate(image, 50)
cv2.imshow('Rotated', rotated)

# flipping
flipped = cv2.flip(image, 0)
cv2.imshow('Flipped', flipped)




cv2.waitKey(0)
