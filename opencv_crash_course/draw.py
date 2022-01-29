import cv2
import numpy as np

# black nothing
blank = np.zeros((500, 500, 3), dtype='uint8')
cv2.imshow('Blank', blank)

# blue nothing
blank[:] = 255, 0, 0
cv2.imshow('blue', blank)

# red square
blank[200:300, 200:300] = 0, 0, 255
cv2.imshow('square', blank)

# a rectangle
cv2.rectangle(blank, (0, 0), (blank.shape[1]//2, blank.shape[0]//4), (255, 255, 0), thickness=-1)
cv2.imshow('rectangle', blank)

# a circle
blank[:] = 0, 0, 0
cv2.circle(blank, (blank.shape[1]//2, blank.shape[0]//4), 40, (255, 0, 255), thickness=10)
cv2.imshow('circle', blank)

# a line
cv2.line(blank, (100, 100), (300, 300), (0, 255, 255), thickness=10)
cv2.imshow('circle', blank)

# some text
cv2.putText(blank, 'Hey yo', (100, 300), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 255, 0), 2)
cv2.imshow('text', blank)

cv2.waitKey(0)
cv2.destroyAllWindows()