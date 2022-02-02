import cv2
import numpy as np

people = ['Sergey', 'Zlata']

haar_cascade = cv2.CascadeClassifier('haarcascade_frontface_default.xml')

# features = np.load('features.npy')
# labels = np.load('labels.npy')

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('face_recognizer.yml')

image = cv2.imread('faces/photo_2022-01-31_12-39-07.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray', gray)

faces_rect = haar_cascade.detectMultiScale(gray, 1.1, 4)

for (x, y, w, h) in faces_rect:
    faces_roi = gray[y:y+h, x:x+w]

    label, confidence = face_recognizer.predict(faces_roi)
    print(f'Label = {label}. Confidence = {confidence}')

    cv2.putText(image, str(people[label]), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), thickness=2)
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), thickness=2)

cv2.imshow('Detected Face', image)
cv2.waitKey(0)
