from typing import Any

import face_recognition
import mariadb
import base64
import io
import pickle

import numpy


def facelogin(capture_image):
    try:
        conn = mariadb.connect(
            user="root",
            password="P@ssw0rd@001",
            host="localhost",
            port=3306,
            database="superai_sampledb"
        )
        cur = conn.cursor()
        known_faces_name = []
        known_faces_encoding: list[Any] = []

        cur.execute("SELECT username, image_encode FROM users")
        for (col1, col2) in cur:
            known_faces_name.append(col1)
            known_faces_encoding.append(pickle.loads(col2))

        conn.close()

        image_capture_string = bytes(capture_image, 'utf-8')
        image_capture_base64 = base64.b64decode(image_capture_string)
        image_capture_byte = io.BytesIO(image_capture_base64)
        image_capture_loading = face_recognition.load_image_file(image_capture_byte)
        image_capture_encoding = face_recognition.face_encodings(image_capture_loading)
        if len(image_capture_encoding) == 0:
            return 'Unknown'

        image_capture_encoding = image_capture_encoding[0]
        results = face_recognition.compare_faces(known_faces_encoding, image_capture_encoding)
        if results.index(True) >= 0:
            distances = face_recognition.face_distance(known_faces_encoding, image_capture_encoding)
            idx_face = numpy.argmin(distances)
            if distances[idx_face] < 0.5:
                found_name = known_faces_name[idx_face]
                return found_name
            else:
                return 'Unknown'
        else:
            return 'Unknown'

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
