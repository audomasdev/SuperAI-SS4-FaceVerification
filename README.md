# Sample Face Verification with Python and OpenCV

## By 405873-ศุภชัย โครงการ SuperAI Season4

## Devlopment Tools
Python
https://www.python.org/downloads/


### Database Tool

Mariadb 
https://mariadb.org/download

Database GUI Tool
dbeaver 
https://dbeaver.io/download/


### Create Table Script
Create database name : superai_sampledb

<code>CREATE TABLE superai_sampledb.users (
	id INT auto_increment NOT NULL,
	username varchar(100) NULL,
	image_encode BLOB NULL,
	CONSTRAINT users_pk PRIMARY KEY (id)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_general_ci;  </code> 

### Required Python Libary
<code>pip install face_recognition
pip install mariadb
pip install cmaker
pip install fastapi
pip install "uvicorn[standard]"
pip install pydantic
pip install numpy
pip install opencv-python
pip install base64
pip install requests
pip install playsound
pip install cv2
</code> 

## How to run 

### Section 1 : Import Picture of user to database
- Go to folder "write-face-to-database/main.py" and then change database connection and save.
- Add user image in folder "user_image" set file name as name of user example "Supachai Singthep.jpg"
- Run _Import.bat or Main.py with any  Python IDE

### Section 2 : Run API (FastAPI)
- Go to Folder "face-detection-verify-api" and chane database connection in facedb.py then save.
- Run _API.bat or API.py with any  Python IDE

### Section 3 : Run UI Application
- Go to "face-detection-verify-api" and run _UI.bat or webcam_face_detection with any Python IDE
