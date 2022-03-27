import matplotlib.pyplot as plt
import cv2
import numpy as np

image = cv2.imread('1.jpg')
# cv2.imshow('Cat', image)

# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imshow('Gray', gray)

blank = np.zeros(image.shape[:2], dtype='uint8')
mask = cv2.circle(blank, (image.shape[1]//2, image.shape[0]//2), 100, 255, -1)
masked = cv2.bitwise_and(image, image, mask=mask)

# gray_hist = cv2.calcHist([gray], [0], mask, [256], [0, 256])

plt.figure()
plt.title('Color Histogram')
plt.xlabel('Bins')
plt.ylabel('# of pixels')
# plt.plot(gray_hist)
# plt.xlim([0, 256])
# plt.show()

colors = ('b', 'g', 'r')
for i, col in enumerate(colors):
    hist = cv2.calcHist([image], [i], mask, [256], [0, 256])
    plt.plot(hist, color=col)
    plt.xlim([0, 256])

plt.show()

cv2.waitKey(0)