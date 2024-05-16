import os
from deepface import DeepFace
import cv2

backends = [
    "opencv",
    "ssd",
    "dlib",
    "mtcnn",
    "fastmtcnn",
    "retinaface",
    "mediapipe",
    "yolov8",
    "yunet",
    "centerface",
]

   
def use_webcam (): # live feed for face detection 
    cap_original = cv2.VideoCapture(1)
    cap= cv2.flip(cap_original, 1)

    try:
        while True:
         ret, frame = cap.read()
         if not ret:
            break
         else:
            faces = DeepFace.extract_faces(img_path = frame, detector_backend = backends[7], enforce_detection=False)
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
            ret, buffer = cv2.imencode('.jpeg', frame)
            frame_bytes = buffer.tobytes()
            yield(b'--frame\r\n'
                        b'Content-Type: image/jepg\r\n\r\n' + frame_bytes + b'\r\n')
            
    finally:
        cap.release()

def face_match (user_input: str): # live feed for face matching
    cap = cv2.VideoCapture(1)
    try:
        while True:
         ret, frame = cap.read()
         if not ret:
            break
         else:
            faces = DeepFace.extract_faces(img_path = frame, detector_backend = backends[7], enforce_detection=False)
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

            if DeepFace.verify(img1_path= frame, img2_path= f"./Database/{user_input}", detector_backend = backends[7], enforce_detection= False)['verified']: # face matching
             cv2.putText(frame, "Match!", (50, 1000), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)
            else:
             cv2.putText(frame, "Not a Match!", (50, 1000), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)

            ret, buffer = cv2.imencode('.jpeg', frame)
            frame_bytes = buffer.tobytes()
            yield(b'--frame\r\n'
                        b'Content-Type: image/jepg\r\n\r\n' + frame_bytes + b'\r\n') 
    finally:
        cap.release()

def makedirectory():
    if not os.path.exists("Database"):
        os.mkdir("Database")
    else:
       pass

def show_images (user_input: str): 
    faces = DeepFace.extract_faces(
    img_path = f"./Database/{user_input}",
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

    cv_img = cv2.imread(f"./Database/{user_input}") 
    for i in range(len(faces)):
        face_with_box = cv2.rectangle(cv_img, (x[i], y[i]), (x[i] + w[i], y[i] + h[i]) , (0,255,0), 2)
    cv2.imwrite("withbox-check.jpg", face_with_box)