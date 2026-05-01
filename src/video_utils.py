from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

import cv2


UPLOAD_TEMP_DIR = Path(tempfile.gettempdir()) / "two_wheeler_violation_demo"


def save_uploaded_video(uploaded_file: Any) -> Path:
    """Persist a Streamlit uploaded file so OpenCV can read it by path."""
    UPLOAD_TEMP_DIR.mkdir(parents=True, exist_ok=True)

    original_name = getattr(uploaded_file, "name", "uploaded_video")
    suffix = Path(original_name).suffix or ".mp4"
    output_path = UPLOAD_TEMP_DIR / f"uploaded_video{suffix.lower()}"

    uploaded_file.seek(0)
    output_path.write_bytes(uploaded_file.read())
    uploaded_file.seek(0)
    return output_path


def get_video_metadata(video_path: Path) -> dict[str, object]:
    metadata: dict[str, object] = {
        "fps": None,
        "total_frames": 0,
        "duration_seconds": None,
        "width": 0,
        "height": 0,
        "resolution": "Unavailable",
        "is_opened": False,
        "error": None,
    }

    capture = cv2.VideoCapture(str(video_path))
    try:
        if not capture.isOpened():
            metadata["error"] = "OpenCV could not open the uploaded video."
            return metadata

        fps = float(capture.get(cv2.CAP_PROP_FPS) or 0.0)
        total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)

        metadata["is_opened"] = True
        metadata["total_frames"] = max(total_frames, 0)
        metadata["width"] = max(width, 0)
        metadata["height"] = max(height, 0)
        metadata["resolution"] = f"{width} x {height}" if width and height else "Unavailable"

        if fps > 0:
            metadata["fps"] = fps
            metadata["duration_seconds"] = total_frames / fps if total_frames > 0 else None

        return metadata
    finally:
        capture.release()


def read_first_frame(video_path: Path):
    capture = cv2.VideoCapture(str(video_path))
    try:
        if not capture.isOpened():
            return None

        success, frame_bgr = capture.read()
        if not success or frame_bgr is None:
            return None

        return cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    finally:
        capture.release()
