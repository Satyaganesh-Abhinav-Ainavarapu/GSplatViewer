import cv2
from pathlib import Path

FRAMES_DIR = Path("frames")
FRAMES_DIR.mkdir(exist_ok=True)
UPLOADS_DIR = Path("uploads")

def extract_frames(video_name):
    video_path = UPLOADS_DIR/video_name
    if not video_path.exists():
        return {
            "status":"failed",
            "error":f"Video file '{video_path}' does not exist."
        }

    video_name = Path(video_name).stem
    video = cv2.VideoCapture(video_path)



    if not video.isOpened():
        raise Exception("Could not open the video")
    
    img_path = FRAMES_DIR/video_name
    img_path.mkdir(parents=True, exist_ok=True)

    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    target_frames = 40 # one frame per degree of rotation
    frame_interval = max(1, total_frames // target_frames)

    
    count=0
    saved_frames=0
    
    success, frame = video.read()
    while success:
        if count%frame_interval==0:
            frame_path = img_path/f"frame_{saved_frames:04d}.jpg"
            cv2.imwrite(str(frame_path), frame)
            saved_frames+=1
        count+=1
        success, frame = video.read()
    video.release()

    return {
        "status": "success",
        "saved_frames": saved_frames,
        "image_folder": str(img_path),
    }