# OpenCV Video Face Recognition Project
**Status:** _under active development_

***

## Project Task:  
#### Make an end-to-end Face Recognition service
## Project details:  
It's going to be a web page, where you can:
* View face recognition algorithm working in realtime (using the server webcam and python RestAPI)
* Manage the Database (see list of registered users, delete/edit them)
* Add user to database (code will parse user's face and store it in DB. Then the algorithm will recognize faces stored in the DB)

***

## Quick start guide:
### 1. Install Python following the instructions on the <a href="https://www.python.org/downloads/">official website</a>
On Windows you also need to add python.exe to PATH. <a href="https://www.educative.io/answers/how-to-add-python-to-path-variable-in-windows">Quick guide</a>
### 2. <a href="https://github.com/LeGGarD/opencv-video-face-recognition-project/archive/refs/heads/develop.zip">Download the project</a> 
### 3. Open the cmd or terminal:
  - On Windows press Win+R, type "cmd" and press Enter
  - On Mac press Command+Space, type "Terminal" and press Enter
### 4. Navigate to the project's directory:
  - Example for Windows: `dir "C:\your_path\opencv-video-face-recognition-project/the_project"`
  - Example for Mac/Linux: `cd your_path/opencv-video-face-recognition-project/the_project` 
### 5. Create Python virtual environment: 
_It is needed to download all libraries and dependencies that the project uses._  
Change `$name` here: `python -m venv ../$name`
### 6. Activate virtual environment:
Be sure to change `$name` here:  
`source ../$name/bin/activate` 
### 7. Install the dependencies:
`pip install -r requirements.txt`
### 8. Run the server:
Check that you are in `opencv-video-face-recognition-project/the_project` directory and your venv is activated. On Linux it looks like this:  
`(venv_name) user@user-pc:~/opencv-video-face-recognition-project/the_project$` 
  
If everything is alright execute:   
`uvicorn main:app`
### 9. Open http://127.0.0.1:8000 in a browser
### 10. Enjoy :)  
  
_Contact me on any questions: mrleggard@gmail.com_

***

## Used things:
Python, OpenCV (cv2), face_recognition, sqlalchemy  
Uvicorn + FastAPI (instead of Flask),  
SQLite, SQLAlchemy  
HTML, CSS, JS, Jinja2
## Development progress:
### Done:
* (✓) Gathering some basic OpenCV knowledge;
* (✓) Coding realtime face recognition algorithm using my own webcam;
* (✓) Investigating methods of streaming video from server to browser;
* (✓) Gathering some basic FastAPI knowledge;
* (✓) Gathering some basic Flask knowledge;
* (✓) Trying to use WebRTC in FastAPI/Flask (found out this way as 'to difficult for me');
* (✓) Using StreamingResponse from FastAPI and <img> tag to stream video;
* (✓) Trying to implement Docker (got some problems because of using SERVER webcam, not CLIENT. I've found out how to pass the webcam into Docker container on Linux, but on Mac and Windows it won't work...);
* (✓) Getting into DB management in FastAPI, code it;
* (✓) Prettifying 2 HTML pages (main + admin for DB);
* (✓) Freaking out with JS to code a start/stop button on the main page;
* (✓) Freaking out with WebSocket after realizing that StreamingResponse isn't the best idea;
* (✓) More dances with start/stop button (now it actually uses your webcam only after pushing the button and actually stops using it, after pushing the stop. Before this, your webcam was used all the time after the server start);
* (✓) Templating HTML pages using Jinja2 syntax;
* (✓) Creation of the 'Add user' page; 
* (✓) Finding out how to pass form data to endpoint; 
* (✓) How to handle freaking redirect after form proceeds post request; 
* (✓) Coding the second step of adding user (face recognition and putting face encoding in DB);
* (✕) Prettifying these two pages; 
* **(✓) Deciding to go the completely different way**
*  (✓) Creation of 1 page with proper form, consisted of a few steps
* (✓) Programming client and backend sides to take photos right inside the form
* (✓) Parsing the taken photos into face encodings
* (✓) Programming a custom form submission with parsed face encodings
* (✓) Adjusting the DB
* (✓) Making some exceptions and restrictions related to the form (like leaving empty fields)
* (✓) Prettifying the visual part of the form
* (✓) Editing main page to be able to recognize faces based on the data stored in DB and show face recognition results in realtime;
* (✓) Separating JS functions for raw webcam stream and the stream with face recognition
* (✓) Doing some performance experiments with webcam stream and face recognition
* (✓) Programming data extraction from the DB
* (✓) Implementing the face recognition service based on the retrieved data
* (✕) Creation of 'Reload DB data' button
* (✓) Reloading face recognition database after adding/removing/editing user
* (✓) Prettifying the final result
### In progress:
* (...) Testing the entire web-platform, debugging, adding exceptions