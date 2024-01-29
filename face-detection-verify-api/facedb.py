from typing import Any
import face_recognition  # เรียกใช้งานไลบรารี face_recognition เพื่อตรวจจับใบหน้า
import mariadb  # เรียกใช้งานไลบรารี mariadb เพื่อเชื่อมต่อฐานข้อมูล
import base64  # เรียกใช้งานไลบรารี base64 เพื่อการจัดการข้อมูลภาพ
import io  # เรียกใช้งานไลบรารี io เพื่อการจัดการข้อมูลอินพุต/เอาต์พุต
import pickle  # เรียกใช้งานไลบรารี pickle เพื่อการทำงานกับข้อมูลที่ถูกซ้อนกัน

import numpy  # เรียกใช้งานไลบรารี numpy เพื่อการทำงานกับอาร์เรย์

# ฟังก์ชันสำหรับการตรวจสอบใบหน้าและเข้าสู่ระบบ
def facelogin(capture_image):
    try:
        # เชื่อมต่อฐานข้อมูล MariaDB
        conn = mariadb.connect(
            user="root",
            password="P@ssw0rd@001",
            host="localhost",
            port=3306,
            database="superai_sampledb"
        )
        cur = conn.cursor()
        known_faces_name = []  # สร้างรายการเพื่อเก็บชื่อใบหน้าที่รู้จัก
        known_faces_encoding: list[Any] = []  # สร้างรายการเพื่อเก็บข้อมูลการเข้ารหัสใบหน้า

        # ดึงข้อมูลชื่อผู้ใช้และข้อมูลภาพจากฐานข้อมูล
        cur.execute("SELECT username, image_encode FROM users")
        for (col1, col2) in cur:
            known_faces_name.append(col1)
            known_faces_encoding.append(pickle.loads(col2))  # โหลดข้อมูลภาพจากการเข้ารหัส

        conn.close()  # ปิดการเชื่อมต่อฐานข้อมูล

        # แปลงข้อมูลภาพที่ได้รับมาเป็นรูปภาพในรูปแบบของ face_recognition
        image_capture_string = bytes(capture_image, 'utf-8')
        image_capture_base64 = base64.b64decode(image_capture_string)
        image_capture_byte = io.BytesIO(image_capture_base64)
        image_capture_loading = face_recognition.load_image_file(image_capture_byte)
        image_capture_encoding = face_recognition.face_encodings(image_capture_loading)
        
        # ถ้ามีใบหน้าที่ตรวจพบ
        if len(image_capture_encoding) == 0:
            return 'Unknown'

        image_capture_encoding = image_capture_encoding[0]  # เลือกข้อมูลการเข้ารหัสใบหน้าตัวแรก
        results = face_recognition.compare_faces(known_faces_encoding, image_capture_encoding)  # เปรียบเทียบใบหน้า
        if results.index(True) >= 0:  # ถ้ามีการตรวจจับใบหน้าที่ตรงกัน
            distances = face_recognition.face_distance(known_faces_encoding, image_capture_encoding)  # คำนวณระยะห่างระหว่างใบหน้า
            idx_face = numpy.argmin(distances)  # หาดัชนีของใบหน้าที่ใกล้เคียงที่สุด
            if distances[idx_face] < 0.5:  # ถ้าระยะห่างน้อยกว่า 0.5
                found_name = known_faces_name[idx_face]  # กำหนดชื่อที่พบ
                return found_name
            else:
                return 'Unknown'  # ถ้าระยะห่างมากกว่า 0.5
        else:
            return 'Unknown'  # ถ้าไม่มีการตรวจจับใบหน้าที่ตรงกัน

    except mariadb.Error as e:  # แสดงข้อผิดพลาดเมื่อเชื่อมต่อกับฐานข้อมูลล้มเหลว
        print(f"Error connecting to MariaDB Platform: {e}")
