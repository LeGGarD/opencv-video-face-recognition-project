import cv2

image = cv2.imread('9.jpg')
cv2.imshow('me', image)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray', gray)

haar_cascade = cv2.CascadeClassifier('haarcascade_frontface_default.xml')

faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10)
print(len(faces_rect))

for (x, y, w, h) in faces_rect:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), thickness=2)

cv2.imshow('Detected', image)

cv2.waitKey(0)
