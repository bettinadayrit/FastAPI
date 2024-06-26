import uvicorn
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent / "src")) # added for docker: ensures that Python can find and import modules from the src directory

if __name__== "__main__":
    uvicorn.run("app.api:app", 
                host= "0.0.0.0", 
                port=8000, 
                reload= True)