import cv2

img_name = '8.jpg'
savepath = 'for saving/' + 'zlata/'

image = cv2.imread(img_name)
cv2.imshow('Cat', image)
# cv2.imwrite('./for saving/cat.jpg', image)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('Cat Gray', gray)
# cv2.imwrite('./for saving/gray_cat.jpg', gray)

# simple thresholding
threshold, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
cv2.imshow('Thresh', thresh)
cv2.imwrite(savepath + 'threshold' + img_name, thresh)

# inverse thresholding
threshold_inv, thresh_inv = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('Thresh Inv', thresh_inv)

# masked = cv2.bitwise_and(image, image, mask=thresh_inv)
# cv2.imshow('Cat2', masked)
# cv2.imwrite('./for saving/masked_cat.jpg', masked)

# adaptive threshold
adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 3)
cv2.imshow('Adaptive Thresh', adaptive_thresh)
cv2.imwrite(savepath + 'adaptive_thresh' + img_name, adaptive_thresh)

# adaptive threshold
adaptive_gaussian_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 3)
cv2.imshow('Adaptive Gauss Thresh', adaptive_gaussian_thresh)
cv2.imwrite(savepath + 'adaptive_gaussian_thresh' + img_name, adaptive_gaussian_thresh)

cv2.waitKey(0)
