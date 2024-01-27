from fastapi import FastAPI
from pydantic import BaseModel
import facedb as fdb
import uvicorn

app = FastAPI()


class FaceloginBody(BaseModel):
    capture_image: str


@app.post("/facelogin")
async def facelogin(param: FaceloginBody):
    return fdb.facelogin(param.capture_image)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)