import os
import face_recognition
import cv2
from typing import List
import numpy as np

KNOWN_FACES_DIR = 'KNOWN_FACES'
# UNKNOWN_FACES_DIR = 'UNKNOWN_FACES'
TOLERANCE = 0.6
FRAME_THIKNESS = 3
FONT_THIKNESS = 2
MODEL = 'hog'


class RecognizeFaces():

    def __init__(self, model: str = 'hog'):
        self.model = model

    def recognize_faces(self, frame: np.ndarray) -> List[np.ndarray]:
        locations = face_recognition.face_locations(frame, model=self.model)
        encodings = face_recognition.face_encodings(frame, locations)
        return encodings
