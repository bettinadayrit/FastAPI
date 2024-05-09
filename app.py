from fastapi import FastAPI
import cv2
from fastapi.responses import StreamingResponse

app = FastAPI()

def use_webcam ():
    cap = cv2.VideoCapture(0)
    try:
        while True:
         ret, frame = cap.read()
         if not ret:
            break
         else: 
            ret, buffer = cv2.imencode('.jpeg', frame)
            frame_bytes = buffer.tobytes()
            yield(b'--frame\r\n'
                  b'Content-Type: image/jepg\r\n\r\n' + frame_bytes + b'\r\n')

    finally:
       cap.release()

@app.get("/")
def index ():
    return {"Welcome!"}

@app.get("/opencv-camera")
def cv_camera():
    return StreamingResponse(use_webcam(), media_type="multipart/x-mixed-replace; boundary=frame")
