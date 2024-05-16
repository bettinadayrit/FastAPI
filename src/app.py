from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import os
import shutil
from deepface import DeepFace
from src.service import use_webcam, face_match, makedirectory, show_images

app = FastAPI()

@app.get("/") 
def index ():
    return {"-- Home Page!"}

@app.get("/opencv-camera") #endpoint: live camera feed for face detection with bounding box
def live_cv_camera():
    return StreamingResponse(
        use_webcam(), media_type="multipart/x-mixed-replace; boundary=frame"
    )

@app.get("/face-matching") #endpoint: live camera feed for face matching 
def live_face_matching(user_input: str):
    return StreamingResponse(
        face_match(user_input), media_type="multipart/x-mixed-replace; boundary=frame"
    )

@app.post("/upload-image")
def upload_file(files: UploadFile= File(...)):
    makedirectory()
    path= os.path.join("Database", files.filename)
    with open (path, 'wb') as file:
        shutil.copyfileobj(files.file, file)
    return{
        'file': files.filename,
        'content': files.content_type,
        'path': path
    }

@app.get("/show-faces") # endpoint: show detected faces for static images 
def static_show_faces(user_input:str):
    show_images(user_input)

@app.get("/comparison-image") # endpoint for face matching (static)
def static_face_match (user_input1: str, user_input2: str):
   result = DeepFace.verify(
    img1_path = f"./Database/{user_input1}",
    img2_path = f"./Database/{user_input2}",
   )
   return {"verification_result": result} 

@app.get("/analyze-image") # endpoint for facial analysis (static)
def static_analyze_images (user_input: str):
    objs = DeepFace.analyze(
    img_path = f"./Database/{user_input}", 
    actions = ['age', 'gender', 'emotion'],
)
    return {"analyzation_result": objs} 
