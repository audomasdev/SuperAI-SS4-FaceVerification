import os  # Import os เพื่อใช้ในการทำงานกับระบบไฟล์
import face_recognition  # Import face_recognition เพื่อการจัดการกับภาพใบหน้า
import mariadb  # Import mariadb เพื่อการเชื่อมต่อฐานข้อมูล MariaDB
import sys  # Import sys เพื่อใช้ในการจัดการกับระบบ
import pickle  # Import pickle เพื่อการทำงานกับข้อมูลที่ถูก Serialize

try:
    # เชื่อมต่อกับฐานข้อมูล MariaDB
    conn = mariadb.connect(
        user="root",
        password="P@ssw0rd@001",
        host="localhost",
        port=3306,
        database="superai_sampledb"
    )
except mariadb.Error as e:  # แสดงข้อผิดพลาดเมื่อไม่สามารถเชื่อมต่อ MariaDB ได้
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)  # ออกจากโปรแกรม

cur = conn.cursor()

try:
    path, filename = os.path.split(__file__)  # แยกทางเข้าแฟ้มจากชื่อไฟล์
    path_user_image = path + "\\user_image\\"  # กำหนดพาธสำหรับภาพผู้ใช้
    file_lists = os.listdir(path_user_image)  # รายการไฟล์ในไดเรกทอรี user_image
    known_faces_encoding = []

    # วนลูปผ่านรายการไฟล์
    for file_list in file_lists:
        img_loaded = face_recognition.load_image_file(path_user_image + file_list)  # โหลดภาพจากไฟล์
        img_encoded = pickle.dumps(face_recognition.face_encodings(img_loaded)[0])  # เข้ารหัสใบหน้า
        sql = "INSERT INTO users (username, image_encode) VALUES (?,?)"  # คำสั่ง SQL
        param = (file_list[0:file_list.rfind(".")], img_encoded)  # พารามิเตอร์สำหรับคำสั่ง SQL
        cur.execute(sql, param)  # ประมวลผลคำสั่ง SQL

except mariadb.Error as e:  # แสดงข้อผิดพลาดเมื่อไม่สามารถดำเนินการได้
    print(f"Error: {e}")

conn.autocommit = False  # ปิดโหมด Auto-commit
conn.commit()  # ยืนยันการเปลี่ยนแปลง
conn.close()  # ปิดการเชื่อมต่อกับฐานข้อมูล
