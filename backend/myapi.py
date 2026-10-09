from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
import cv2

app = FastAPI()

UPLOAD_DIR = Path("uploads")
FRAMES_DIR = Path("frames")
UPLOAD_DIR.mkdir(exist_ok=True)
FRAMES_DIR.mkdir(exist_ok=True)


def extract_frames(video_path, video_name):
    video_name = Path(video_name).stem
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        raise Exception("Could not open the video")
    img_path = FRAMES_DIR/video_name
    img_path.mkdir(parents=True, exist_ok=True)
    count=0
    success, frame = video.read()
    while success:
        frame_path = img_path/f"frame_{count:04d}.jpg"
        cv2.imwrite(str(frame_path), frame)
        count+=1
        success, frame = video.read()
    video.release()
    return count

@app.get("/")
def h3():
    return{"default":"This should've been the home page --fastapi"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    file_path = UPLOAD_DIR / file.filename
    file_path.write_bytes(contents)

    frame_count =   extract_frames(file_path, file.filename)

    return{
        "message" : "upload successful",
        "filename": file.filename,
        "content_type": file.content_type,  
        "frames_extracted": frame_count
    }

