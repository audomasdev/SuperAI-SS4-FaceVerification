import base64
import threading
import cv2
from time import sleep
import os
import requests
import numpy as np

# กำหนดพาธของไฟล์ haarcascade_frontalface_default.xml สำหรับใช้ในการตรวจจับใบหน้า
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

# เปิดการใช้งานกล้องเว็บแคมและกำหนดค่า fps, width, height
video_capture = cv2.VideoCapture(0)
fps = video_capture.get(cv2.CAP_PROP_FPS)
width = int(video_capture.get(3))
height = int(video_capture.get(4))
fps = int(video_capture.get(5))

# กำหนดพื้นที่สี่เหลี่ยมที่ต้องการให้ตรวจจับใบหน้า
sq = 330
area_x1 = int((width / 2) - (sq / 2)) + 20
area_y1 = int((height / 2) - (sq / 2))
area_x2 = area_x1 + sq
area_y2 = area_y1 + sq
face_hold = 20
count_hold = 0

# โหลดโลโก้และกำหนดตัวแปรเก็บชื่อใบหน้า
path, filename = os.path.split(__file__)
logo = cv2.imread('bg.png')
face_name = ''

# ฟังก์ชันสำหรับล้างค่าใบหน้า
def clear_name():
    global face_name
    face_name = ''

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    ret, frame = video_capture.read()
    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # ตรวจจับใบหน้า
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(220, 220)
    )

    frame = cv2.addWeighted(frame, 1, logo, 0, 0)

    if len(faces) == 1:
        x, y, w, h = faces[0]
        if x > area_x1 and y > area_y1 and (x + w) < area_x2 and (y + h) < area_y2:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            count_hold = count_hold + 1
            if count_hold >= face_hold:
                # ทำการดึงใบหน้าออกจากรูปภาพและลดขนาดให้เหลือ 200x200 pixels
                face = gray[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (200, 200))
                # แปลงรูปใบหน้าเป็น base64 เพื่อส่งไปยังเซิร์ฟเวอร์
                retval, buffer_img = cv2.imencode('.jpg', face_resize)
                data = base64.b64encode(buffer_img)

                url = 'http://localhost:8000/facelogin'
                param = {"capture_image": str(data.decode('utf-8'))}
                x = requests.post(url, json=param)
                face_name = x.text.replace('"', '')
                print("------------------------")

                if face_name != "Internal Server Error":
                    print(face_name)
                elif face_name == "Internal Server Error":
                    face_name = "Unknown"
                    print("Unknown")

                threading.Timer(5, clear_name).start()
        else:
            count_hold = 0
    else:
        count_hold = 0

    # แสดงชื่อใบหน้าบนเฟรมวิดีโอ
    cv2.putText(
        img=frame,
        text=face_name,
        org=(area_x1 + 80, 440),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.7,
        color=(0, 255, 0),
        thickness=2)

    # แสดงวีดีโอที่ได้หลังจากประมวลผล
    cv2.imshow('Video', frame)

    if count_hold >= face_hold:
        count_hold = 0

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# เมื่อทุกอย่างเสร็จสิ้น Release
video_capture.release()
cv2.destroyAllWindows()
