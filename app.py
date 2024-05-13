from fastapi import FastAPI
import cv2
from fastapi.responses import StreamingResponse
from deepface import DeepFace

app = FastAPI()

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

def use_webcam (mirror=False):
    cap = cv2.VideoCapture(1)

    if mirror:
        frame= cv2.flip(frame, 1)

    try:
        while True:
         ret, frame = cap.read()
         if not ret:
            break
         else:
            result = DeepFace.verify(img1_path= frame, img2_path= "test.jpg", detector_backend = backends[7], enforce_detection= False)
            for face in result:
                if "region" in face:
                    x, y, w, h = map(int, face["region"])
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
         
         txt = str(result)
         cv2.putText(frame, txt, (50,50), cv2.FONT_HERSHEY_SIMPLEX,1, (0,255,0),2 )
         ret, buffer = cv2.imencode('.jpeg', frame)
         frame_bytes = buffer.tobytes()
         yield(b'--frame\r\n'
                  b'Content-Type: image/jepg\r\n\r\n' + frame_bytes + b'\r\n')
            
    finally:
      cap.release()
        #cv2.imshow("Face Detection", frame) 

@app.get("/")
def index ():
    return {"-- Home Page!"}

@app.get("/opencv-camera")
def cv_camera():
    return StreamingResponse(use_webcam(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/comparison-image") ## test endpoint for facial recog (static)
def compare_images ():
   result = DeepFace.verify(
    img1_path = "img3.jpeg",
    img2_path = "img2.jpeg",
     model_name = models[1],
   )
   return {"verification_result": result} 

@app.get("/analyze-image") ## test endpoint for facial analysis (static)
def analyze_images ():
    objs = DeepFace.analyze(
    img_path = "img2.jpeg", 
    actions = ['age', 'gender', 'race', 'emotion'],
)
    return {"analyzation_result": objs} 

@app.get("/extract-image") ## test endpoint for face extraction
def extract_images ():
    face = DeepFace.extract_faces(
    img_path = "img2.jpeg", 
    detector_backend = backends[7]
)
    return {"extraction_result": face}