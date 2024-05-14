from fastapi import FastAPI, File, UploadFile
import cv2
from fastapi.responses import StreamingResponse, FileResponse
from deepface import DeepFace
import uuid
import os
from random import randint

app = FastAPI()
db= []

models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",
  "GhostFaceNet",
]

backends = [
  'opencv', 
  'ssd', 
  'dlib', 
  'mtcnn', 
  'fastmtcnn',
  'retinaface', 
  'mediapipe',
  'yolov8',
  'yunet',
  'centerface',
]

def use_webcam (mirror=False): # live feed and face matching
    cap = cv2.VideoCapture('rtsp://192.168.1.250:554/h264')

    if mirror:
        frame= cv2.flip(frame, 1)

    if cap.isOpened: # checking if: the camera is opened // usual error: stream timeout triggered after 30s, but camera is opened
       print("Camera is opened")
    else:
       print("Failed streaming")

    try:
        while True:
         ret, frame = cap.read()
         if not ret:
            break
        
        faces = DeepFace.extract_faces(img_path = frame, detector_backend = backends[7])
        x = []
        y = []
        w = []
        h = []
        for face in faces:
         x.append(face['facial_area']['x'])
         y.append(face['facial_area']['y'])
         w.append(face['facial_area']['w'])
         h.append(face['facial_area']['h'])

        for i in range(len(faces)):
            cv2.rectangle(frame, (x[i], y[i]), (x[i] + w[i], y[i] + h[i]) , (0,255,0), 2)

        if DeepFace.verify(img1_path= frame, img2_path= "img2.jpg", detector_backend = backends[7], enforce_detection= False)['verified']: # face matching
            cv2.putText(frame, "MATCH!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

        ret, buffer = cv2.imencode('.jpeg', frame)
        frame_bytes = buffer.tobytes()
        yield(b'--frame\r\n'
                  b'Content-Type: image/jepg\r\n\r\n' + frame_bytes + b'\r\n')
        
    finally:
      cap.release()
   
@app.get("/") 
def index ():
    return {"-- Home Page!"}

@app.get("/opencv-camera") #endpoint: live camera feed
def cv_camera():
    return StreamingResponse(use_webcam(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/show-faces") # test end point for face detection
def show_images (): # test code for function: detect faces in a STATIC image + generation of bounding box for every face detected
    faces = DeepFace.extract_faces(
    img_path = "img3.jpg", 
    detector_backend = backends[7],
)
    print(faces)
    x = []
    y = []
    w = []
    h = []
    for face in faces:
        x.append(face['facial_area']['x'])
        y.append(face['facial_area']['y'])
        w.append(face['facial_area']['w'])
        h.append(face['facial_area']['h'])

    cv_img = cv2.imread("img3.jpg") 
    for i in range(len(faces)):
        face_with_box = cv2.rectangle(cv_img, (x[i], y[i]), (x[i] + w[i], y[i] + h[i]) , (0,255,0), 2)
    cv2.imwrite("withbox-check.jpg", face_with_box)


@app.get("/comparison-image") # test endpoint for facial recog (static)
def compare_images ():
   result = DeepFace.verify(
    img1_path = "img3.jpeg",
    img2_path = "img2.jpeg",
     model_name = models[1],
   )
   return {"verification_result": result} 

@app.get("/analyze-image") # test endpoint for facial analysis (static)
def analyze_images ():
    objs = DeepFace.analyze(
    img_path = "img1.jpg", 
    actions = ['age', 'gender', 'emotion', 'race'],
)
    return {"analyzation_result": objs} 

@app.get("/extract-image") # test endpoint for face extraction (static)
def extract_images ():
    face = DeepFace.extract_faces(
    img_path = "img2.jpg", 
    detector_backend = backends[7]
)
    return {"Faces present": len(face)}

@app.post("/upload-image")
async def create_upload_file(file: UploadFile = File(...)):
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read() 
    db.append(contents)
    return {"filename": file.filename}
