# OpenCV Video Face Recognition Project  
  
**Status:** _under active development_

## Project Task:  
#### Make an end-to-end Face Recognition service  
  
## Project details:  
It's going to be a web page, where you can:
* View face recognition algorithm working in realtime (using the server webcam and python RestAPI)
* Manage the Database (see list of registered users, delete/edit them)
* Add user to database (code will parse user's face and store it in DB. Then the algorithm will recognize faces stored in the DB)

## Quick start guide:
coming soon... 

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
### In progress:
* (...) _Creation of the 'Add user' page;_ 
  * (✓) _Finding out how to pass form data to endpoint;_ 
  * (✓) _How to handle freaking redirect after form proceeds post request;_ 
  * (✓) _Coding the second step of adding user (face recognition and putting face encoding in DB);_ 
  * (✕) _Prettifying these two pages;_ 
  * **(✓) _Deciding to go the completely different way_**
  * (✓) _Creation of 1 page with proper form, consisted of a few steps_
  * (✓) _Programming client and backend sides to take photos right inside the form_
  * (✓) _Parsing the taken photos into face encodings_
  * (✓) _Programming a custom form submission with parsed face encodings_
  * (✓) _Adjusting the DB_
  * (✓) _Making some exceptions and restrictions related to the form (like leaving empty fields)_
  * (...) _Prettifying the visual part of the form_
* (...) _Editing main page to be able to recognize faces based on the data stored in DB and show face recognition results in realtime;_ 
  * (✓) _Separating JS functions for raw webcam stream and the stream with face recognition_
  * (✓) _Doing some performance experiments with webcam stream and face recognition_
  * (✓) _Programming data extraction from the DB_
  * (✓) _Implementing the face recognition service based on the retrieved data_
  * (...) _Creation of 'Reload DB data' button_
  * (...) _Prettifying the final result_
  
## Used things:  
Python, OpenCV (cv2), face_recognition, sqlalchemy 
Uvicorn + FastAPI (instead of Flask),  
SQLite, SQLAlchemy  
HTML, CSS, JS, Jinja2
