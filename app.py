from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import cv2
from fastapi.responses import StreamingResponse
import asyncio
import uvicorn

app = FastAPI()

def use_webcam ():
    cap = cv2.VideoCapture(0)

    try:
        while True:
         ret, frame = cap.read()
         if not ret:
            break
         
        # converting captured frames into jpeg
         ret, buffer = cv2.imencode('.jpeg', frame)
         frame_bytes = buffer.tobytes()

        ## streamable response

         yield(b'--frame\r\n'
              b'Content-Type: image/jepg\r\n\r\n' + frame_bytes + b'\r\n')

    finally:
       cap.release()

@app.get("/")
def index ():
    return {"Welcome!"}

@app.get("/opencv-camera")
def use_webcam():
    return StreamingResponse(use_webcam(), media_type="multipart/x-mixed-replace; boundary=frame")