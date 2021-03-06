import sqlite3
import time
import cv2
import numpy as np
import face_recognition
import json
import sqlalchemy
from sqlalchemy.orm import Session

from sql import models, crud, database
from sql.database import SessionLocal


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
        self.TOLERANCE = 0.5
        self.FONT_SCALE = 0.6
        self.MODEL = 'hog'
        self.COLOR = [0, 255, 0]
        self.db_data = self.reload_database()
        self.len_db_data = len(self.db_data['encodings'])
        self.time_from_last_face_rec_update = time.time()
        self.last_face_rec_results = None
        print(f'service_get_webcam_stream.generate_frame_face_rec(): Quantity of encodings in the db_data -> '
              f'{len(self.db_data["encodings"])}')
        print(f'service_get_webcam_stream.generate_frame_face_rec(): Quantity of encodings in the DB -> '
              f'{len(crud.get_face_encodings(db=SessionLocal()))}')

    def start_stream(self) -> bool:
        """
        Starts the webcam stream
        """
        self.webcam = cv2.VideoCapture(0)
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
        self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
        self.webcam.set(cv2.CAP_PROP_FPS, 30)
        print('service_get_webcam_stream.start_stream(): Webcam has turned on!')
        return True

    def stop_stream(self) -> bool:
        """
        Stops the webcam stream
        """
        self.webcam.release()
        print('service_get_webcam_stream.stop_stream(): Webcam has turned off!')
        return True

    def reload_database(self, db: Session = SessionLocal()) -> dict:
        """
        Reloads the list of all known face encodings and the dict with indices of users + their names and addresses
        """

        def query_db():
            # Querying the DB to get all names, addresses and encodings
            all_encodings_ = db.query(models.FaceEncoding.face_encoding).all()
            all_names_ = db.query(models.User.name).all()
            all_addresses_ = db.query(models.User.address).all()
            return all_encodings_, all_names_, all_addresses_

        try:
            # Trying to query
            all_encodings, all_names, all_addresses = query_db()
            # If the DB is empty or absent, initialize it first
        except sqlalchemy.exc.OperationalError or sqlite3.OperationalError as e:
            database.Base.metadata.create_all(database.engine)
            all_encodings, all_names, all_addresses = query_db()

        encodings = []
        for encoding in all_encodings:
            encodings.append(json.loads(encoding[0]))

        names = [x[0] for x in all_names]
        addresses = [x[0] for x in all_addresses]

        map_index_to_user = {key: value for key, value in zip(range(len(all_names)), zip(names, addresses))}

        self.len_db_data = len(all_names)
        db.close()
        print('service_get_webcam_stream.reload_database(): The data from the DB was updated!')
        # print(f'service_get_webcam_stream.reload_database(): {len(encodings)}')
        return {'encodings': encodings, 'index_to_user': map_index_to_user}

    def put_text_(self, frame, text, org, color=(108, 158, 20)):
        cv2.putText(img=frame, text=text, org=org, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=self.FONT_SCALE,
                    color=(0, 0, 0), lineType=cv2.LINE_AA, thickness=3)
        cv2.putText(img=frame, text=text, org=org, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=self.FONT_SCALE,
                    color=color, lineType=cv2.LINE_AA, thickness=2)

    async def generate_frame_bytes(self) -> bytes or None:
        """
        Returns the actual webcam frame encoded as png and then as bytes

        Is used in resource_webcam_stream.websocket_endpoint() if stream_type == 1
        """
        try:
            success, frame = self.webcam.read()
            frame = cv2.flip(frame, 1)
            ret, png_frame = cv2.imencode('.png', frame)
            bytes_frame = png_frame.tobytes()
            return bytes_frame
        except:
            return None

    async def generate_frame_face_rec(self, db: Session = SessionLocal()) -> bytes or None:
        """
        Returns the actual webcam frame encoded as png and then as bytes
        It also has names and addresses of recognized captured people

        Performance measurements on i5-8300H:
        - raw frame generation takes ~0.035 sec
        - frame with located face in it takes ~0.43 sec
        - frame with located and recognized from DB face takes ~0.6 sec

        Performance measurements on M1:
        - raw frame generation takes ~0.07 sec
        - frame with located face in it takes ~0.32 sec
        - frame with located and recognized from DB face takes ~0.33 sec

        Is used in resource_webcam_stream.websocket_endpoint() if stream_type == 2
        """
        try:
            # trying to retrieve a frame from the webcam
            t1 = time.time()
            success, frame = self.webcam.read()
            frame = cv2.flip(frame, 1)

            # recognize faces if it was more than 1 seconds from the last face rec update
            # print(f'service_get_webcam_stream.generate_frame_face_rec(): Time from the last face rec update -> '
            #       f'{time.time() - self.time_from_last_face_rec_update}')
            if time.time() - self.time_from_last_face_rec_update > 1:
                locations = face_recognition.face_locations(frame, model=self.MODEL)
                encodings = face_recognition.face_encodings(frame, locations)
                self.last_face_rec_results = ['Residents aren\'t found', ]

                if self.len_db_data > 0:
                    for face_encoding in encodings:
                        # print(type(self.db_data['encodings'][0]))
                        # print(type(self.db_data['encodings'][0][0]))
                        # print(type(face_encoding))
                        # print(type(face_encoding[0]))
                        results = face_recognition.face_distance(np.array(self.db_data['encodings']),
                                                                 np.array(face_encoding))
                        distances = []
                        for i in range(0, len(results), 5):
                            mean_distance = np.mean(results[i:i + 5])
                            distances.append(mean_distance)
                        min_distance = np.min(distances)

                        if min_distance < self.TOLERANCE:
                            matched_identity_idx = distances.index(np.min(distances))
                            name = self.db_data['index_to_user'][matched_identity_idx][0]
                            address = self.db_data['index_to_user'][matched_identity_idx][1]
                            print(f'service_get_webcam_stream.generate_frame_face_rec(): User found: {name}, {address}')
                            if self.last_face_rec_results[0] == 'Residents aren\'t found':
                                self.last_face_rec_results = ['Found 1 or more residents:', ]
                            self.last_face_rec_results.append((name, address))

                    self.time_from_last_face_rec_update = time.time()

            padding = 0
            for person in self.last_face_rec_results:
                if isinstance(person, str):
                    text = person
                    self.put_text_(frame, text, (20, 40 + padding), color=(255, 255, 255))
                else:
                    text = f'{person[0]}, {person[1]}'
                    self.put_text_(frame, text, (20, 40 + padding))
                padding += 30

            ret, png_frame = cv2.imencode('.png', frame)
            bytes_frame = png_frame.tobytes()
            t2 = time.time()
            # print(f'service_get_webcam_stream.generate_frame_face_rec(): Frame generation took {t2 - t1} sec')
            return bytes_frame
        except:
            return None

    def generated_frame(self) -> np.ndarray or None:
        """
        Returns the actual webcam frame

        Is used in resource_webcam_stream.take_photo()
        """
        try:
            success, frame = self.webcam.read()
            frame = cv2.flip(frame, 1)
            return frame
        except:
            return None
