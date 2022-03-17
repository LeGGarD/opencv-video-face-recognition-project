import os
import face_recognition
import cv2
from injectable import injectable

KNOWN_FACES_DIR = 'KNOWN_FACES'
# UNKNOWN_FACES_DIR = 'UNKNOWN_FACES'
TOLERANCE = 0.6
FRAME_THIKNESS = 3
FONT_THIKNESS = 2
MODEL = 'hog'


@injectable
class RecognizeFaces():
    video = cv2.VideoCapture(0)

    def add_face(self):
        # print('loading known faces...')
        #
        # known_faces = []
        # known_names = []
        #
        # for name in os.listdir(KNOWN_FACES_DIR):
        #     for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):
        #         image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')
        #         encoding = face_recognition.face_encodings(image)
        #         known_faces.append(encoding[0])
        #         known_names.append(name)


    def load_faces(self):
        pass

    def recognize_faces(self):
        print('processing unknown faces...')

        while True:
            # print(filename)
            # image = face_recognition.load_image_file(f'{UNKNOWN_FACES_DIR}/{filename}')

            ret, image = video.read()

            locations = face_recognition.face_locations(image, model=MODEL)
            encodings = face_recognition.face_encodings(image, locations)
            # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            for face_encoding, face_location in zip(encodings, locations):
                results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
                match = None
                if True in results:
                    match = known_names[results.index(True)]
                    print(f'Match found: {match}')
                    top_left = (face_location[3], face_location[0])
                    bottom_right = (face_location[1], face_location[2])
                    color = [0, 255, 0]
                    cv2.rectangle(image, top_left, bottom_right, color, FRAME_THIKNESS)

                    top_left = (face_location[3], face_location[2])
                    bottom_right = (face_location[1], face_location[2] + 22)
                    cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
                    cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (200, 200, 200), FONT_THIKNESS)

            cv2.imshow('Webcam', image)
            if cv2.waitKey(20) & 0xFF == ord('d'):
                break
            # cv2.waitKey(0)
            # cv2.destroyWindow(filename)
