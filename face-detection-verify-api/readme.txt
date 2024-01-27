pip install face_recognition
pip install mariadb
pip install cmaker

##
pip install fastapi
pip install "uvicorn[standard]"
pip install pydantic
pip install numpy
pip install opencv-python
pip install base64
pip install requests
pip install playsound
pip install cv2
##

CREATE TABLE superai_sampledb.users (
	id INT auto_increment NOT NULL,
	username varchar(100) NULL,
	image_encode BLOB NULL,
	CONSTRAINT users_pk PRIMARY KEY (id)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_general_ci;
