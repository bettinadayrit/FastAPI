from fastapi import FastAPI
import cv2
from fastapi.responses import StreamingResponse, Response
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
         else:
            result = DeepFace.verify(img1_path= frame, img2_path= "test.jpg", detector_backend = backends[7], enforce_detection= False) # face matching
            for face in result: 
                if "region" in face: # generation of bounding box for faces detected in the result, not working --
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

def show_images (): # test code for function: detect faces in a static image + generation of bounding box for every face detected
    faces = DeepFace.extract_faces(
    img_path = "img2.jpg", 
    detector_backend = backends[7],
)
    print(faces)
    face_data = faces[0]['facial_area']
    cv_img = cv2.imread("img2.jpg")
    #print(face_data) ## error: face_data has too many values -> need to extract x, y, w, and h ONLY
    x1, y1, width, height = face_data[0].values() # error -- too many values 
    face_with_box = cv2.rectangle(cv_img, (x1, y1), (x1 + width, y1 + height) , (0,255,0), 2)
    
    cv2.imwrite("withbox.jpg", face_with_box)


@app.get("/") 
def index ():
    return {"-- Home Page!"}

@app.get("/opencv-camera") #endpoint: live camera feed
def cv_camera():
    return StreamingResponse(use_webcam(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/show-faces") # test endpoint: showing processed imgs for bounding box generation
def get_image():
    return Response(show_images(), media_type="image/png")

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
