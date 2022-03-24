import cv2
import face_recognition


class WebcamStream():

    def __init__(self):
        self.webcam = None
        self.webcam_resolution = None

    def resize_webcam_resolution(self, frame, needed_height: int = 540):
        resolution = frame.shape
        coef = needed_height / resolution[0]
        return int(resolution[1] * coef), int(resolution[0] * coef)

    def start_stream(self):
        self.webcam = cv2.VideoCapture(0)
        _, frame = self.webcam.read()
        self.webcam_resolution = self.resize_webcam_resolution(frame)
        print(f'Webcam has turned on! With {self.webcam_resolution} resolution')

    def generated_frame(self):
        success, frame = self.webcam.read()

        # locations = face_recognition.face_locations(frame, model='small')
        #
        # for face_location in locations:
        #     top_left = (face_location[3], face_location[0])
        #     bottom_right = (face_location[1], face_location[2])
        #     color = [0, 255, 0]
        #     cv2.rectangle(frame, top_left, bottom_right, color, 3)

        frame = cv2.resize(frame, self.webcam_resolution, interpolation=cv2.INTER_CUBIC)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        return frame

    def stop_stream(self):
        self.webcam.release()
        print('Webcam has turned off!')
