from pathlib import Path
import subprocess

COLMAP_DIR = Path("colmap")
COLMAP_DIR.mkdir(exist_ok=True)
FRAMES_DIR = Path("frames")


def run_colmap(video_name):
    video_name = Path(video_name).stem

    image_folder = FRAMES_DIR / video_name
    if not image_folder.exists():
        return {
            "status": "failed",
            "error": f"Image folder '{image_folder}' does not exist."
        }

    work_dir = COLMAP_DIR / video_name
    work_dir.mkdir(exist_ok=True)

    db_path = work_dir / "database.db"
    sparse_dir = work_dir / "sparse"
    sparse_dir.mkdir(parents=True, exist_ok=True)

    # Final PLY file
    ply_path = work_dir / "model.ply"

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

    cmd_convert = [
        "colmap", "model_converter",
        "--input_path", str(sparse_dir / "0"),
        "--output_path", str(ply_path),
        "--output_type", "PLY",
    ]

    pipeline = [
        ("Feature Extraction", cmd_extract),
        ("Sequential Matching", cmd_match),
        ("3D Mapping", cmd_map),
    ]

    for step_name, command in pipeline:
        print(f"Running {step_name}...")

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            print(result.stderr)
            return {
                "status": "failed",
                "step": step_name,
                "error": result.stderr.strip(),
            }

        print(f"{step_name} completed successfully")

    if not (sparse_dir / "0").exists():
        return {
            "status": "failed",
            "error": "No sparse model generated",
        }

    print("Running Model Converter...")

    result = subprocess.run(cmd_convert, capture_output=True, text=True)

    if result.returncode != 0:
        print(result.stderr)
        return {
            "status": "failed",
            "step": "Model Conversion",
            "error": result.stderr.strip(),
        }

    if not ply_path.exists():
        return {
            "status": "failed",
            "error": "PLY file was not generated",
        }

    print("Model Conversion completed successfully")

    return {
        "status": "success",
        "database": str(db_path),
        "sparse_path": str(sparse_dir / "0"),
        "ply_path": str(ply_path),
    }