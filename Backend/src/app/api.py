import os
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware 
from app.service import makedirectory
from app.test import liveness_check, verification_result_storage
from dotenv import load_dotenv

load_dotenv()

# database directory -- for: dockerfile
BASE_DIR = os.getenv("BASE_DIR", "Database")
os.makedirs(BASE_DIR, exist_ok=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins = ["*"],
    allow_credentials= True,
    allow_methods= ["*"],
    allow_headers= ["*"]
)

@app.get("/") # endpoint: "homepage"
async def index():
    return {"Hello!"}

@app.get("/face-verification") # endpoint: liveness checking + face detector/matching 
def live_face_verification(user_input: str):
    return StreamingResponse(liveness_check(user_input), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/verification-result")  # endpoint: showing results as string 
def get_verification_result():
    return JSONResponse(content=verification_result_storage)

@app.post("/upload-image") #endpoint: uploading images  
def upload_file(files: UploadFile= File(...)):
    makedirectory()
    path= os.path.join(BASE_DIR, files.filename) 
    with open (path, 'wb') as file:
        shutil.copyfileobj(files.file, file)
    return{
        'file': files.filename,
       'content': files.content_type,
        'path': path
    }