import cv2


class WebcamStream:

    def __init__(self):
        self.webcam = None

    def start_stream(self) -> bool:
        self.webcam = cv2.VideoCapture(0)
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
        self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
        self.webcam.set(cv2.CAP_PROP_FPS, 30)
        return True

    async def generated_frame_bytes(self) -> bytes or None:
        try:
            success, frame = self.webcam.read()
            frame = cv2.flip(frame, 1)
            ret, png_frame = cv2.imencode('.png', frame)
            bytes_frame = png_frame.tobytes()
            return bytes_frame
        except:
            return None

    def stop_stream(self) -> bool:
        self.webcam.release()
        print('Webcam has turned off!')
        return True
