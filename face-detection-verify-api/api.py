from fastapi import FastAPI  # เรียกใช้งาน FastAPI เพื่อสร้าง API
from pydantic import BaseModel  # เรียกใช้งาน BaseModel เพื่อกำหนดโมเดลข้อมูล
import facedb as fdb  # เรียกใช้งาน facedb สำหรับการตรวจสอบใบหน้า
import uvicorn  # เรียกใช้งาน uvicorn เพื่อเรียกใช้งานเซิร์ฟเวอร์

app = FastAPI()  # สร้างแอปพลิเคชัน FastAPI


class FaceloginBody(BaseModel):  # กำหนดโมเดลข้อมูลสำหรับรับข้อมูลการลงชื่อเข้าใช้
    capture_image: str  # รับข้อมูลภาพใบหน้าเป็นสตริง

# เส้นทาง API สำหรับการตรวจสอบใบหน้า
@app.post("/facelogin")
async def facelogin(param: FaceloginBody):
    return fdb.facelogin(param.capture_image)  # เรียกใช้งานฟังก์ชัน facelogin จาก facedb

# เรียกใช้งาน uvicorn เพื่อเริ่มต้นเซิร์ฟเวอร์ FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
