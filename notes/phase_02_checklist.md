# Phase 2 Checklist - Video Upload and Frame Reading

## Phase Goal

Use OpenCV to read the uploaded video and display basic video metadata in the Streamlit app.

This phase must not include YOLO inference, model loading, helmet detection, rider counting, ALPR, OCR, tracking, PDF generation, email sending, or SMS logging.

## Source Documents Read Before This Phase

- [x] `docs/01_system_requirements.md`
- [x] `docs/02_system_architecture.md`
- [x] `docs/03_development_phases.md`
- [x] `docs/09_fps_benchmark.md`
- [x] `docs/10_streamlit_ui_design.md`
- [x] `docs/11_folder_structure.md`

## Files and Folders Expected Before Starting

- [x] `app.py`
- [x] `requirements.txt`
- [x] `README.md`
- [x] `.gitignore`
- [x] `.env.example`
- [x] `data/mock_owner_registry.json`
- [x] `src/__init__.py`
- [x] `models/`
- [x] `data/`
- [x] `src/`
- [x] `outputs/`
- [x] `outputs/challans/`
- [x] `outputs/evidence/`
- [x] `outputs/processed_videos/`
- [x] `sample_videos/`

## Files to Create or Modify in Phase 2

- [x] Modify `app.py`
- [x] Modify `requirements.txt`
- [x] Create `src/video_utils.py`
- [x] Optional: update `README.md` with Phase 2 run notes

## Dependency Changes

Add OpenCV and supporting packages to `requirements.txt`:

```text
opencv-python
numpy
Pillow
```

Keep existing Phase 1 dependency:

```text
streamlit>=1.33
```

Do not add:

- [x] `ultralytics`
- [x] `easyocr`
- [x] `reportlab`
- [x] `python-dotenv`
- [x] email/SMS libraries

Those belong to later phases.

## Video Upload Requirements

- [x] Continue using Streamlit sidebar uploader.
- [x] Supported formats remain:
  - [x] `.mp4`
  - [x] `.avi`
  - [x] `.mov`
  - [x] `.mkv`
- [x] Uploaded video should be saved to a temporary local file before OpenCV reads it.
- [x] Temporary file should preserve the uploaded file extension when possible.
- [x] The app should handle no-upload state cleanly.
- [x] The app should handle unreadable/corrupt video gracefully.

## Video Metadata Requirements

After upload, display:

- [x] Uploaded file name
- [x] Input video FPS
- [x] Total frames
- [x] Duration in seconds
- [x] Width
- [x] Height
- [x] Resolution as `width x height`

Required formulas:

```text
duration_seconds = total_frames / input_fps
resolution = width x height
```

If FPS is missing or zero:

- [x] Do not crash.
- [x] Display FPS as unavailable.
- [x] Display duration as unavailable.

## Preview Requirements

Display at least one preview:

- [x] Uploaded video preview using Streamlit, if supported by the uploaded format.
- [x] First readable frame extracted with OpenCV.

Frame display rules:

- [x] OpenCV reads frames as BGR.
- [x] Convert BGR to RGB before passing frame to Streamlit.
- [x] If the first frame cannot be read, show a clear error message.

## `src/video_utils.py` Requirements

Create reusable helper functions for video handling.

Required functions:

```python
save_uploaded_video(uploaded_file) -> Path
get_video_metadata(video_path: Path) -> dict
read_first_frame(video_path: Path)
```

Suggested metadata dictionary keys:

```python
{
    "fps": float | None,
    "total_frames": int,
    "duration_seconds": float | None,
    "width": int,
    "height": int,
    "resolution": str,
    "is_opened": bool,
    "error": str | None,
}
```

Implementation rules:

- [x] Use OpenCV only for reading video metadata and first frame.
- [x] Release `cv2.VideoCapture` after use.
- [x] Do not keep video files open.
- [x] Do not start detection loops.
- [x] Do not process every frame yet.

## Streamlit UI Requirements

Update the existing Video Upload section to show:

- [x] Uploaded file name
- [x] Video preview or first frame preview
- [x] Metadata panel/table
- [x] Clear status message when no file is uploaded
- [x] Clear warning/error if OpenCV cannot read the uploaded file

Recommended metadata display:

- [x] Use `st.metric` or a simple table for:
  - [x] FPS
  - [x] Total frames
  - [x] Duration
  - [x] Resolution

## Forbidden in This Phase

- [x] Do not load `models/two-wheeler.pt`.
- [x] Do not load `models/helmet-detection.pt`.
- [x] Do not load `models/alpr.pt`.
- [x] Do not load `models/yolov8n-pose.pt`.
- [x] Do not import `ultralytics`.
- [x] Do not run YOLO inference.
- [x] Do not implement two-wheeler detection.
- [x] Do not implement tracking.
- [x] Do not implement expanded bike+rider regions.
- [x] Do not implement helmet detection.
- [x] Do not implement pose rider counting.
- [x] Do not implement ALPR.
- [x] Do not implement EasyOCR.
- [x] Do not generate PDF challans.
- [x] Do not send email.
- [x] Do not create SMS logs.
- [x] Do not add live camera input.

## Acceptance Criteria

- [ ] App runs using:

```bash
streamlit run app.py
```

- [ ] User can upload a supported video.
- [x] App saves uploaded video temporarily for OpenCV reading.
- [x] App displays input FPS when available.
- [x] App displays total frames.
- [x] App displays duration when FPS is valid.
- [x] App displays width, height, and resolution.
- [x] App displays a video preview or first extracted frame.
- [x] App handles invalid/unreadable video without crashing.
- [x] Mock owner registry from Phase 1 still works.
- [x] No detection/model/OCR/notification functionality exists yet.

## Manual Test Plan

1. Start the app from the project root:

```bash
streamlit run app.py
```

2. Confirm the app loads.
3. Confirm the mock owner registry still displays.
4. Upload a valid `.mp4`, `.avi`, `.mov`, or `.mkv` file.
5. Confirm the uploaded filename appears.
6. Confirm FPS is displayed, or marked unavailable if the file has no valid FPS.
7. Confirm total frame count is displayed.
8. Confirm duration is displayed when FPS is valid.
9. Confirm resolution is displayed.
10. Confirm a preview frame or video preview appears.
11. Try an invalid file renamed as a video, if available.
12. Confirm the app shows a clean error instead of crashing.

## Verification Commands

Run from:

```text
D:\codexWorkspace\Demo
```

Syntax check:

```bash
py -m py_compile app.py src/video_utils.py
```

Forbidden import scan:

```powershell
Select-String -Path app.py,src\*.py -Pattern 'ultralytics|YOLO|easyocr|reportlab|smtplib|twilio|pytesseract|paddleocr' -CaseSensitive:$false
```

Expected result:

```text
No forbidden imports should appear.
```

## Completion Notes

Fill this after Phase 2 is implemented:

```text
Completed files:
app.py, requirements.txt, README.md, src/config.py, src/mock_database.py, src/video_utils.py

Verification performed:
AST syntax checks passed for app.py, src/config.py, src/mock_database.py, and src/video_utils.py. OpenCV video utility functions were tested with a generated 5-frame AVI. Mock owner registry helpers were tested under the workspace tmp folder. Forbidden import scan found no YOLO, EasyOCR, PDF, email, or SMS libraries.

Known limitations:
Streamlit is not installed in the current Python environment, so `streamlit run app.py` could not be verified here. OpenCV, NumPy, and Pillow are available.

Next phase:
Phase 3 - Two-Wheeler Detection
```
