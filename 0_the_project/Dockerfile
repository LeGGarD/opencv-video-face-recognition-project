FROM python:3.9.10

# Install dependencies
RUN python3 -m pip install --upgrade pip
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install fastapi
RUN pip install uvicorn
RUN pip install opencv-python
RUN pip install cmake
RUN pip install Jinja2
RUN pip install injectable
RUN pip install sqlite3
RUN pip install sqlalchemy
# Install dlib and face_recognition
RUN git clone https://github.com/davisking/dlib.git
WORKDIR dlib
RUN mkdir build
WORKDIR build
RUN cmake ..; cmake --build .
WORKDIR ..
RUN python3 setup.py install
RUN pip install face_recognition

# Main app
COPY . /app
WORKDIR /app

# Run command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]