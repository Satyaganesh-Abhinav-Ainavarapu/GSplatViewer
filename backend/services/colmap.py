from pathlib import Path
import subprocess

COLMAP_DIR = Path("colmap")
COLMAP_DIR.mkdir(exist_ok=True)
FRAMES_DIR = Path("frames")


def run_colmap(video_name):
    video_name = Path(video_name).stem
    image_folder = FRAMES_DIR/video_name
    if not image_folder.exists():
        return{
            "status":"failed",
            "error":f"Image folder '{image_folder}' does not exist."
        }
    
    work_dir = COLMAP_DIR/video_name
    work_dir.mkdir(exist_ok=True)
    
    db_path = work_dir/"database.db"  #Paths Setup
    sparse_dir = work_dir/"sparse"
    sparse_dir.mkdir(exist_ok=True, parents=True)

    cmd_extract = [
        "colmap", "feature_extractor",
        "--database_path", str(db_path),
        "--image_path", str(image_folder),
        "--ImageReader.single_camera", "1",
    ]
    
    cmd_match = [
        "colmap", "sequential_matcher",
        "--database_path", str(db_path),
        "--SequentialMatching.loop_detection", "1",
    ]
    
    cmd_map = [
        "colmap", "mapper",
        "--database_path", str(db_path),
        "--image_path", str(image_folder),
        "--output_path", str(sparse_dir),
    ]

    pipeline=[
        ("Feature Extraction", cmd_extract),
        ("Sequential Matching", cmd_match),
        ("3D Mapping", cmd_map),
    ]

    for step_name, command in pipeline:
        print(f"Running {step_name}...")
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode!=0:
            print(result.stderr)
            return {
                "status":"failed",
                "step":step_name,
                "error":result.stderr.strip(),
            }
        print(f"{step_name} completed successfully")

    if not (sparse_dir/"0").exists():
        return {
            "status":"failed",
            "error":"No sparse model generated",
        }
    

    return {
        "status":"success",
        "sparse_path": str(sparse_dir/"0"),
        "database": str(db_path),
    }