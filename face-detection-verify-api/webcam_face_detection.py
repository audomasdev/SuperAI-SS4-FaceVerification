import base64  # นำเข้าโมดูล base64 เพื่อการจัดการข้อมูลภาพ
import threading  # นำเข้าโมดูล threading เพื่อการประมวลผลแบบพร้อมกัน

import cv2  # นำเข้า OpenCV เพื่อการจัดการภาพ
from time import sleep  # นำเข้า sleep เพื่อการหยุดรอ
import os  # นำเข้าโมดูล os เพื่อการทำงานกับระบบไฟล์
import requests  # นำเข้า requests เพื่อการส่งคำขอ HTTP
import numpy as np  # นำเข้า numpy เพื่อการทำงานกับอาร์เรย์

# ตัวแปรที่ใช้ในการตรวจจับใบหน้า
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

# เปิดกล้อง
video_capture = cv2.VideoCapture(0)
fps = video_capture.get(cv2.CAP_PROP_FPS)  # อ่าน frames per second (fps) จากกล้อง
width = int(video_capture.get(3))  # ความกว้างของภาพ
height = int(video_capture.get(4))  # ความสูงของภาพ
fps = int(video_capture.get(5))  # fps ที่จริง

sq = 330  # ความยาวของสี่เหลี่ยมจัตุรัสที่ใช้ในการตรวจจับใบหน้า
area_x1 = int((width / 2) - (sq / 2)) + 20  # ตำแหน่ง x ด้านซ้ายของสี่เหลี่ยมจัตุรัส
area_y1 = int((height / 2) - (sq / 2))  # ตำแหน่ง y ด้านบนของสี่เหลี่ยมจัตุรัส
area_x2 = area_x1 + sq  # ตำแหน่ง x ด้านขวาของสี่เหลี่ยมจัตุรัส
area_y2 = area_y1 + sq  # ตำแหน่ง y ด้านล่างของสี่เหลี่ยมจัตุรัส
face_hold = 20  # จำนวนเฟรมที่จำเป็นในการตรวจจับใบหน้า
count_hold = 0  # จำนวนเฟรมที่มีใบหน้า

path, filename = os.path.split(__file__)  # แยก path และ filename จากไฟล์ที่กำลังทำงาน
face_name = ''  # ตัวแปรเก็บชื่อใบหน้า

# ฟังก์ชันสำหรับล้างชื่อใบหน้า
def clear_name():
    global face_name
    face_name = ''

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')  # แสดงข้อความเมื่อไม่สามารถโหลดกล้องได้
        sleep(5)  # หยุดรอ 5 วินาที
        pass

    ret, frame = video_capture.read()  # อ่านภาพจากกล้อง
    frame = cv2.flip(frame, 1)  # พลิกภาพ

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # แปลงภาพเป็นสีเทา
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(220, 220)
    )

    if len(faces) == 1:  # ถ้ามีใบหน้าตรวจพบ 1 ใบ
        x, y, w, h = faces[0]  # ดึงพิกัดและขนาดของใบหน้า
        if x > area_x1 and y > area_y1 and (x + w) < area_x2 and (y + h) < area_y2:  # ตรวจสอบว่าใบหน้าอยู่ในพื้นที่ที่กำหนด
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # วาดสี่เหลี่ยมบนใบหน้า
            count_hold = count_hold + 1  # เพิ่มจำนวนเฟรมที่มีใบหน้า
            if count_hold >= face_hold:  # ถ้ามีเฟรมมากกว่าหรือเท่ากับค่า face_hold
                face = gray[y:y + h, x:x + w]  # ดึงส่วนใบหน้าออกมา
                face_resize = cv2.resize(face, (200, 200))  # เปลี่ยนขนาดใบหน้าเป็น 200x200 pixels
                retval, buffer_img = cv2.imencode('.jpg', face_resize)  # แปลงภาพเป็นรูปแบบ JPEG
                data = base64.b64encode(buffer_img)  # เข้ารหัสภาพเป็น base64

                url = 'http://localhost:8000/facelogin'  # URL สำหรับส่งข้อมูลภาพ
                param = {"capture_image": str(data.decode('utf-8'))}  # พารามิเตอร์สำหรับการส่งข้อมูล
                x = requests.post(url, json=param)  # ส่งคำขอ POST ไปยัง URL
                face_name = x.text.replace('"', '')  # รับชื่อใบหน้าจากการตอบกลับ

                if face_name != "Internal Server Error":  # ถ้าไม่มีข้อผิดพลาดภายในเซิร์ฟเวอร์
                    print(face_name)  # แสดงชื่อใบหน้า
                elif face_name == "Internal Server Error":  # ถ้ามีข้อผิดพลาดภายในเซิร์ฟเวอร์
                    face_name = "Unknown"  # กำหนดให้เป็น "Unknown"
                    print("Unknown")  # แสดงข้อความ "Unknown"

                threading.Timer(5, clear_name).start()  # สร้างเธรดเพื่อล้างชื่อใบหน้าหลังจาก 5 วินาที
        else:
            count_hold = 0  # รีเซ็ตค่า count_hold เป็น 0
    else:
        count_hold = 0  # รีเซ็ตค่า count_hold เป็น 0

    # แสดงชื่อใบหน้าบนภาพ
    cv2.putText(
        img=frame,
        text=face_name,
        org=(area_x1 + 80, 440),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.7,
        color=(0, 255, 0),
        thickness=2)

    cv2.imshow('Video', frame)  # แสดงภาพผ่านหน้าต่าง 'Video'

    if count_hold >= face_hold:  # ถ้ามีเฟรมมากกว่าหรือเท่ากับค่า face_hold
        count_hold = 0  # รีเซ็ตค่า count_hold เป็น 0

    if cv2.waitKey(1) & 0xFF == ord('q'):  # หยุดการทำงานเมื่อกด 'q'
        break

# ปิดการใช้งานกล้องและหน้าต่าง
video_capture.release()
cv2.destroyAllWindows()
