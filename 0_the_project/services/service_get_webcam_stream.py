import cv2


class WebcamStream:

    def __init__(self):
        self.webcam = cv2.VideoCapture(0)

    def resize_webcam_resolution(self, camera: cv2.VideoCapture, needed_height: int = 540):
        success, frame = camera.read()
        resolution = frame.shape
        coef = needed_height / resolution[0]
        return int(resolution[1] * coef), int(resolution[0] * coef)

    def generate_frames(self):
        while True:

            ## read the camera frame
            success, frame = self.webcam.read()
            if not success:
                break
            else:

                # locations = face_recognition.face_locations(frame, model='small')
                #
                # for face_location in locations:
                #     top_left = (face_location[3], face_location[0])
                #     bottom_right = (face_location[1], face_location[2])
                #     color = [0, 255, 0]
                #     cv2.rectangle(frame, top_left, bottom_right, color, 3)

                frame = cv2.resize(frame, self.resize_webcam_resolution(self.webcam), interpolation=cv2.INTER_CUBIC)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n'
                   + frame +
                   b'\r\n')