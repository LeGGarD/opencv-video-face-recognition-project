import cv2
from typing import Tuple
import numpy
import face_recognition
import numpy as np


class WebcamStream():

    def __init__(self):
        self.webcam = None
        self.webcam_resolution = None

    def resize_webcam_resolution(self, frame: numpy.ndarray, needed_height: int = 540) -> Tuple[int, int]:
        resolution = frame.shape
        coef = needed_height / resolution[0]
        return int(resolution[1] * coef), int(resolution[0] * coef)

    def start_stream(self) -> bool:
        self.webcam = cv2.VideoCapture(0)
        _, frame = self.webcam.read()
        self.webcam_resolution = self.resize_webcam_resolution(frame)
        print(f'Webcam has turned on! With {self.webcam_resolution} resolution')
        return True

    def generated_frame_bytes(self) -> bytes:
        buffer = self.generated_frame()
        frame = buffer.tobytes()
        return frame

    def generated_frame(self) -> np.ndarray:
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
        return buffer

    def stop_stream(self) -> bool:
        self.webcam.release()
        print('Webcam has turned off!')
        return True
