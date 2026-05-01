# Phase 3 Checklist - Two-Wheeler Detection

## Phase Goal

Load `models/two-wheeler.pt` using Ultralytics YOLO and run two-wheeler detection on uploaded video frames.

This phase should draw two-wheeler bounding boxes and display annotated output. It must not include helmet detection, rider counting, ALPR, OCR, tracking, challan generation, email, or SMS.

## Source Documents to Read Before This Phase

- [x] `docs/01_system_requirements.md`
- [x] `docs/02_system_architecture.md`
- [x] `docs/03_development_phases.md`
- [x] `docs/04_model_details.md`
- [x] `docs/10_streamlit_ui_design.md`
- [x] `docs/11_folder_structure.md`
- [x] `notes/phase_01_checklist.md`
- [x] `notes/phase_02_checklist.md`

## Required Model File

Before implementation, confirm this file exists:

```text
models/two-wheeler.pt
```

Checklist:

- [x] `models/two-wheeler.pt` exists.
- [x] Filename matches exactly: `two-wheeler.pt`.
- [x] Do not rename code to fit a different model filename.
- [x] Do not load helmet, ALPR, or pose models in this phase.

## Files to Create or Modify in Phase 3

- [x] Modify `requirements.txt`
- [x] Modify `src/config.py`
- [x] Create `src/detector.py`
- [x] Modify `app.py`
- [x] Optional: update `README.md` with Phase 3 notes
- [x] Update this checklist after implementation

## Dependency Changes

Add Ultralytics to `requirements.txt`:

```text
ultralytics
```

Keep existing dependencies:

```text
streamlit>=1.33
opencv-python
numpy
Pillow
```

Do not add:

- [x] `easyocr`
- [x] `reportlab`
- [x] `python-dotenv`
- [ ] email/SMS libraries

Those belong to later phases.

## `src/config.py` Requirements

Confirm or add:

```python
TWO_WHEELER_MODEL_PATH = MODELS_DIR / "two-wheeler.pt"
TWO_WHEELER_CONFIDENCE = 0.35
```

Rules:

- [x] Model path should come from config.
- [x] Confidence default should come from config.
- [x] UI may allow changing confidence threshold.

## `src/detector.py` Requirements

Create a detector module for YOLO model loading and two-wheeler inference.

Required responsibilities:

- [x] Import Ultralytics YOLO only in `src/detector.py`.
- [x] Load `models/two-wheeler.pt`.
- [x] Validate model file exists before loading.
- [x] Return a clear error if the model file is missing.
- [x] Run inference on a frame.
- [x] Filter detections by confidence threshold.
- [x] Return two-wheeler boxes in frame coordinates.
- [x] Do not decide violations.
- [x] Do not create track IDs.
- [x] Do not load other models.

Recommended detection result structure:

```python
{
    "box": [x1, y1, x2, y2],
    "confidence": 0.91,
    "class_id": 0,
    "class_name": "bike"
}
```

Required functions:

```python
load_two_wheeler_model()
detect_two_wheelers(frame_rgb_or_bgr, model, confidence_threshold: float) -> list[dict]
draw_two_wheeler_boxes(frame_rgb, detections: list[dict])
```

Implementation notes:

- [x] Load the model once per run, not once per frame.
- [x] Keep output coordinates as integers.
- [x] Draw boxes on a copy of the frame.
- [x] Use a clear label such as `Bike 0.91`.
- [x] Return RGB output for Streamlit display.

## Streamlit UI Requirements

Update the app to include:

- [x] Sidebar two-wheeler confidence slider.
- [x] Default slider value from `TWO_WHEELER_CONFIDENCE`.
- [x] Start detection button.
- [x] Clear message if video is uploaded but detection has not started.
- [x] Clear error if `models/two-wheeler.pt` is missing.
- [x] Annotated frame display after detection.
- [x] Detection count for the displayed frame.

Recommended Phase 3 behavior:

- [x] Use the first readable frame for initial two-wheeler detection.
- [x] Display original first frame from Phase 2.
- [x] Display annotated first frame after clicking Start Detection.
- [x] Do not process the full video yet unless needed for display.

Reason:

```text
Full video/frame-loop benchmarking is Phase 4. Phase 3 should prove model loading, inference, and bounding-box drawing first.
```

## Video Handling Requirements

Reuse Phase 2 utilities:

- [ ] `save_uploaded_video`
- [ ] `get_video_metadata`
- [ ] `read_first_frame`

Rules:

- [x] Do not duplicate video metadata logic in `app.py`.
- [x] Do not start full frame-by-frame processing in Phase 3.
- [x] Do not save processed videos yet.

## Bounding Box Drawing Requirements

Annotated frame should show:

- [x] Rectangle around detected two-wheeler.
- [x] Label with class name and confidence.
- [x] Detection count near the output.

Drawing rules:

- [x] Use RGB frame for Streamlit display.
- [x] If drawing with OpenCV, use RGB-compatible colors intentionally.
- [x] Do not mutate the original preview frame in place.

## Forbidden in This Phase

- [x] Do not load `models/helmet-detection.pt`.
- [x] Do not load `models/alpr.pt`.
- [x] Do not load `models/yolov8n-pose.pt`.
- [x] Do not implement helmet detection.
- [x] Do not classify helmet status.
- [x] Do not implement expanded bike+rider region.
- [x] Do not implement pose rider counting.
- [x] Do not implement ALPR.
- [x] Do not implement EasyOCR.
- [x] Do not implement OCR fallback plate.
- [x] Do not implement tracking.
- [x] Do not assign track IDs.
- [x] Do not implement duplicate challan control.
- [x] Do not implement violation logic.
- [x] Do not generate PDF challans.
- [x] Do not send email.
- [x] Do not create SMS logs.
- [x] Do not add live camera input.
- [x] Do not claim real-time capability yet.

## Acceptance Criteria

- [ ] App runs using:

```bash
streamlit run app.py
```

- [ ] User can upload a supported video.
- [ ] Phase 2 metadata still displays correctly.
- [x] User can set two-wheeler confidence threshold.
- [x] User can click Start Detection.
- [x] App loads `models/two-wheeler.pt`.
- [ ] App detects two-wheelers on the first readable frame.
- [x] App draws two-wheeler bounding boxes.
- [x] App displays detection count.
- [x] App handles missing model file without crashing.
- [x] App handles frames with zero detections cleanly.
- [x] No helmet, pose, ALPR, OCR, tracking, challan, email, or SMS code exists.

## Manual Test Plan

1. Confirm model file exists:

```powershell
Test-Path D:\codexWorkspace\Demo\models\two-wheeler.pt
```

2. Start the app:

```bash
streamlit run app.py
```

3. Upload a valid traffic video.
4. Confirm metadata still displays.
5. Confirm the first frame preview appears.
6. Adjust the two-wheeler confidence slider.
7. Click Start Detection.
8. Confirm annotated frame appears.
9. Confirm detection count appears.
10. Try a very high confidence threshold.
11. Confirm zero-detection state is handled cleanly.
12. Temporarily rename the model file and rerun.
13. Confirm missing-model error is shown cleanly.
14. Rename the model file back to `two-wheeler.pt`.

## Verification Commands

Run from:

```text
D:\codexWorkspace\Demo
```

Syntax check:

```bash
py -m py_compile app.py src/config.py src/mock_database.py src/video_utils.py src/detector.py
```

Forbidden import scan:

```powershell
Select-String -Path app.py,src\*.py,requirements.txt -Pattern 'easyocr|reportlab|smtplib|twilio|pytesseract|paddleocr|helmet-detection|alpr.pt|yolov8n-pose|track_id|challan|sms' -CaseSensitive:$false
```

Expected result:

```text
No forbidden later-phase implementation should appear.
```

Allowed in this phase:

```text
ultralytics
YOLO
models/two-wheeler.pt
cv2
```

## Completion Notes

Fill this after Phase 3 is implemented:

```text
Completed files:
app.py, requirements.txt, README.md, src/config.py, src/detector.py, notes/phase_03_checklist.md

Verification performed:
Confirmed `models/two-wheeler.pt` exists with the required filename. Installed/verified requirements in the active Python environment. Parsed app.py, src/config.py, src/mock_database.py, src/video_utils.py, and src/detector.py successfully with Python AST syntax validation. Loaded `models/two-wheeler.pt` through `src/detector.py`, ran inference on a blank frame, and verified annotated-frame output. Ran detection against `tmp/phase2_test.avi` first frame and verified the zero-detection path. Verified missing model handling raises a clear FileNotFoundError. Forbidden later-phase implementation scan returned no matches in app.py, src/*.py, or requirements.txt. Started Streamlit with `py -m streamlit run app.py --server.port 8501 --server.headless true` and confirmed HTTP 200 from `http://127.0.0.1:8501`.

Known limitations:
`py -m py_compile ...` could not be completed in this Windows sandbox because Python was denied permission while renaming generated `.pyc` files in `__pycache__`, so AST syntax validation was used instead. The Streamlit startup check verified the app shell, but detection was not manually verified through the browser upload flow on a real traffic video with visible two-wheelers in this run.

Next phase:
Phase 4 - FPS Benchmark
```
