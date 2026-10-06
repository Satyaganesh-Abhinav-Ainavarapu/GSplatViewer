from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, HTTPException
import shutil
from pathlib import Path

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def h3():
    return{"default":"This should've been the home page --fastapi"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    file_path = UPLOAD_DIR / file.filename

    file_path.write_bytes(contents)

    return{
        "message" : "upload successful",
        "filename": file.filename,
        "content_type": file.content_type
    }

