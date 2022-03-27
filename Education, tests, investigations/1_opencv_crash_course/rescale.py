import cv2

def rescale_image(frame, size=0.75):
    width = int(frame.shape[1] * size)
    height = int(frame.shape[0] * size)
    dimensions = (width, height)
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

# def change_resolution(width, height):
#     capture.set(3, width)
#     capture.set(4, height)

image = cv2.imread('1.jpg')
image_resized = rescale_image(image, 2)

cv2.imshow('Cat', image)
cv2.imshow('Cat Resized', image_resized)
cv2.waitKey(0)
cv2.destroyWindow('Cat')

# capture = cv2.VideoCapture(0)
#
# while True:
#     isTrue, frame = capture.read()
#     cv2.imshow('Webcam', frame)
#     cv2.imshow('Webcam Resized', rescale_image(frame, size=2))
#
#     if cv2.waitKey(20) & 0xFF==ord('q'):
#         break
#
# capture.release()
# cv2.destroyAllWindows()
