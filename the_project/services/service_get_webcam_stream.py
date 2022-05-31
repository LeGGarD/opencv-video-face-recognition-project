import time
import cv2
import numpy as np
import face_recognition
import json
from fastapi import Depends

from sql import models
from sql.database import SessionLocal
from sqlalchemy.orm import Session


# Dependency
def get_db():
    db_ = SessionLocal()
    try:
        yield db_
    finally:
        db_.close()


class WebcamStream:

    def __init__(self):
        self.webcam = None
        self.TOLERANCE = 0.6
        self.FRAME_THIKNESS = 3
        self.FONT_THIKNESS = 2
        self.MODEL = 'hog'
        self.COLOR = [0, 255, 0]
        self.db_data = self.reload_database()
        self.time_from_last_face_rec_update = time.time()
        self.last_face_rec_results = None

    def start_stream(self) -> bool:
        '''
        Starts the webcam stream
        '''
        self.webcam = cv2.VideoCapture(0)
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
        self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
        self.webcam.set(cv2.CAP_PROP_FPS, 30)
        print('service_get_webcam_stream.start_stream(): Webcam has turned on!')
        return True

    def stop_stream(self) -> bool:
        '''
        Stops the webcam stream
        '''
        self.webcam.release()
        print('service_get_webcam_stream.stop_stream(): Webcam has turned off!')
        return True

    def reload_database(self, db: Session = SessionLocal()) -> dict:
        '''
        Reloads the database with faces that needed to be recognized and owners' data
        '''
        all_encodings = db.query(models.FaceEncoding.face_encoding).all()
        all_names = db.query(models.User.name).all()
        all_addresses = db.query(models.User.address).all()
        fin_encodings = []
        fin_names = []
        fin_addresses = []
        for encoding in all_encodings:
            fin_encodings.append(json.loads(encoding[0]))
        for name in all_names:
            for i in range(5):
                fin_names.append(name[0])
        for address in all_addresses:
            for i in range(5):
                fin_addresses.append(address[0])
        db.close()
        print('service_get_webcam_stream.reload_database(): The data from the DB was updated!')
        return {'encodings': fin_encodings, 'names': fin_names, 'addresses': fin_addresses}

    async def generate_frame_bytes(self) -> bytes or None:
        '''
        Returns the actual webcam frame encoded as png and then as bytes

        Is used in resource_webcam_stream.websocket_endpoint() if stream_type == 1
        '''
        try:
            success, frame = self.webcam.read()
            frame = cv2.flip(frame, 1)
            ret, png_frame = cv2.imencode('.png', frame)
            bytes_frame = png_frame.tobytes()
            return bytes_frame
        except:
            return None

    async def generate_frame_face_rec(self) -> bytes or None:
        '''
        Returns the actual webcam frame encoded as png and then as bytes
        It also has the rectangles around recognized faces, names and adresses of recognized captured people

        Performance measurements on i5-8300H:
        - raw frame generation takes ~0.035 sec
        - frame with localed face in it takes ~0.43 sec
        - frame with located and recognized from DB face takes ~0.6 sec

        Performance measurements on M1:
        - raw frame generation takes ~0.07 sec
        - frame with localed face in it takes ~0.32 sec
        - frame with located and recognized from DB face takes ~0.33 sec

        Is used in resource_webcam_stream.websocket_endpoint() if stream_type == 2
        '''
        try:
            t1 = time.time()
            # trying to retrieve a frame from the webcam
            success, frame = self.webcam.read()
            frame = cv2.flip(frame, 1)

            # locations = face_recognition.face_locations(frame, model=self.MODEL)
            # for face_location in locations:
            #     top_left = (face_location[3], face_location[0])
            #     bottom_right = (face_location[1], face_location[2])
            #     color = [0, 255, 0]
            #     cv2.rectangle(frame, top_left, bottom_right, color, self.FRAME_THIKNESS)

            # recognize faces if it was more than 0.3 seconds from the last face rec update
            # if time.time() - self.time_from_last_face_rec_update > 0.3:
            # locations = face_recognition.face_locations(frame, model=self.MODEL)
            # encodings = face_recognition.face_encodings(frame, locations)
            #
            # for face_encoding, face_location in zip(encodings, locations):
            #     results = face_recognition.compare_faces(self.db_data['encodings'], face_encoding, self.TOLERANCE)
            #     match = None
            #     if True in results:
            #         match = self.db_data['names'][results.index(True)]
            #         print(f'service_get_webcam_stream.generate_frame_face_rec(): Match found: {match}')
            #         top_left = (face_location[3], face_location[0])
            #         bottom_right = (face_location[1], face_location[2])
            #         color = [0, 255, 0]
            #         cv2.rectangle(frame, top_left, bottom_right, color, self.FRAME_THIKNESS)
            #
            #         top_left = (face_location[3], face_location[2])
            #         bottom_right = (face_location[1], face_location[2] + 22)
            #         cv2.rectangle(frame, top_left, bottom_right, color, cv2.FILLED)
            #         cv2.putText(frame, match, (face_location[3] + 10, face_location[2] + 15),
            #                     cv2.FONT_HERSHEY_SIMPLEX,
            #                     0.5,
            #                     (200, 200, 200), self.FONT_THIKNESS)

            ret, png_frame = cv2.imencode('.png', frame)
            bytes_frame = png_frame.tobytes()
            t2 = time.time()
            print(f'service_get_webcam_stream.generate_frame_face_rec(): Frame generation took {t2 - t1} sec')
            return bytes_frame
        except:
            return None

    def generated_frame(self) -> np.ndarray or None:
        '''
        Returns the actual webcam frame

        Is used in resource_webcam_stream.take_photo()
        '''
        try:
            success, frame = self.webcam.read()
            frame = cv2.flip(frame, 1)
            return frame
        except:
            return None
