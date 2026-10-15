from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
from services.video import extract_frames
from services.colmap import run_colmap

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

    frame_count = extract_frames(file.filename)

    colmap_result = run_colmap(file.filename)

    return{
        "message" : "upload successful",
        "filename": file.filename,
        "content_type": file.content_type,  
        "frames_extracted": frame_count,
        "colmap": colmap_result,
    }

