import os
import face_recognition
import mariadb
import sys
import pickle

try:
    conn = mariadb.connect(
        user="root",
        password="P@ssw0rd@001",
        host="localhost",
        port=3306,
        database="superai_sampledb"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()

try:
    path, filename = os.path.split(__file__)
    path_user_image = path + "\\user_image\\"
    file_lists = os.listdir(path_user_image)
    known_faces_encoding = []
    for file_list in file_lists:
        img_loaded = face_recognition.load_image_file(path_user_image + file_list)
        img_encoded = pickle.dumps(face_recognition.face_encodings(img_loaded)[0])
        sql = "INSERT INTO users (username, image_encode) VALUES (?,?)"
        param = (file_list[0:file_list.rfind(".")], img_encoded)
        cur.execute(sql, param)
except mariadb.Error as e:
    print(f"Error: {e}")

conn.autocommit = False
conn.commit()
conn.close()
