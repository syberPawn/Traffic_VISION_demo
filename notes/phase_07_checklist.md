# Phase 7 Checklist - Pose-Based Rider Counting

## Phase Goal

Load `models/yolov8n-pose.pt` using Ultralytics YOLO and count riders associated with each detected two-wheeler's expanded bike+rider region.

This phase should display rider count per detected bike and mark triple riding when the rider count is greater than or equal to 3.

This phase must not include ALPR, OCR, tracking, violation confirmation, duplicate challan control, PDF generation, email, or SMS.

## Source Documents Read Before This Phase

- [x] `docs/01_system_requirements.md`
- [x] `docs/02_system_architecture.md`
- [x] `docs/03_development_phases.md`
- [x] `docs/04_model_details.md`
- [x] `docs/06_violation_logic.md`
- [x] `docs/10_streamlit_ui_design.md`
- [x] `docs/11_folder_structure.md`
- [x] `notes/phase_06_checklist.md`

## Required Model File

Before implementation, confirm this file exists:

```text
models/yolov8n-pose.pt
```

Checklist:

- [x] `models/yolov8n-pose.pt` exists.
- [x] Filename matches exactly: `yolov8n-pose.pt`.
- [x] Do not rename code to fit a different model filename.
- [x] Do not load `models/alpr.pt` in this phase.
- [x] Keep using `models/two-wheeler.pt` for bike detection.
- [x] Keep using `models/helmet-detection.pt` for helmet status.

## Current Codebase State Before Phase 7

- [x] `app.py` coordinates Streamlit upload, metadata, first-frame detection, expanded regions, helmet detection, FPS benchmark, and owner registry.
- [x] `src/detector.py` loads two-wheeler and helmet models.
- [x] `src/region_utils.py` creates clipped expanded bike+rider regions.
- [x] `src/benchmark.py` runs full-video two-wheeler FPS benchmarking only.
- [x] `src/config.py` already contains `POSE_CONFIDENCE = 0.25`.
- [x] `README.md` currently marks rider counting as not included yet.

## Files to Create or Modify in Phase 7

- [x] Modify `src/config.py`
- [x] Modify `src/detector.py`
- [x] Modify `src/region_utils.py`
- [x] Modify `app.py`
- [x] Optional: modify `README.md`
- [x] Update this checklist after implementation

Recommended config addition:

```python
POSE_MODEL_PATH = MODELS_DIR / "yolov8n-pose.pt"
```

## Dependency Changes

No new dependency should be required.

Keep existing dependencies:

```text
streamlit>=1.33
opencv-python
numpy
Pillow
ultralytics
```

Do not add:

- [x] `easyocr`
- [x] `reportlab`
- [x] `python-dotenv`
- [x] email/SMS libraries
- [x] tracking libraries

Those belong to later phases.

## Pose Detector Requirements

Add pose model support without breaking the existing detectors.

Required responsibilities:

- [x] Import Ultralytics YOLO only in `src/detector.py`.
- [x] Load `models/yolov8n-pose.pt`.
- [x] Validate pose model file exists before loading.
- [x] Return a clear error if the pose model file is missing.
- [x] Load the pose model once per app run, not once per bike.
- [x] Run pose inference once on the full frame by default.
- [x] Extract person detections with boxes and available keypoints.
- [x] Filter person detections by `POSE_CONFIDENCE`.
- [x] Do not decide violations.
- [x] Do not generate challans.
- [x] Do not create track IDs.

Recommended functions:

```python
load_pose_model()
detect_person_poses(frame_rgb, model, confidence_threshold: float) -> list[dict]
count_riders_for_region(person_poses: list[dict], expanded_region: list[int]) -> int
```

Recommended pose result structure:

```python
{
    "box": [x1, y1, x2, y2],
    "confidence": 0.88,
    "class_id": 0,
    "class_name": "person",
    "center": [cx, cy],
    "keypoints": [[x, y], [x, y]]
}
```

## Rider Association Requirements

The pose model detects people, not riders. Rider counting must be based on association with each bike's expanded region.

- [x] Count only pose detections associated with the current bike's expanded region.
- [x] Do not count all persons in the frame.
- [x] Associate a person when their body center is inside the expanded region.
- [x] Also allow association when sufficient valid keypoints fall inside the expanded region.
- [x] Handle missing keypoints gracefully.
- [x] Return `rider_count` per bike.
- [x] Mark `triple_riding` as true when `rider_count >= 3`.
- [x] Do not convert triple riding into confirmed violation rows in this phase.

## Streamlit UI Requirements

Update the app to include:

- [x] Sidebar pose confidence slider.
- [x] Default slider value from `POSE_CONFIDENCE`.
- [x] Start Detection should run:
  - [x] Two-wheeler detection.
  - [x] Expanded bike+rider region generation.
  - [x] Helmet detection on each expanded region.
  - [x] Pose inference once on the full first frame.
  - [x] Rider count association for each expanded region.
- [x] Show original bike boxes.
- [x] Show expanded bike+rider regions.
- [x] Show helmet status per detected two-wheeler.
- [x] Show rider count per detected two-wheeler.
- [x] Show `Triple Riding` label/status when `rider_count >= 3`.
- [x] Show clear error if `models/yolov8n-pose.pt` is missing.
- [x] Keep FPS Benchmark available.

## FPS Benchmark Boundary

Phase 4 FPS benchmark may remain a two-wheeler benchmark unless explicitly expanded.

- [x] Do not silently change benchmark meaning.
- [x] If pose inference is added to the benchmark, label it clearly as a two-wheeler + helmet + pose benchmark.
- [x] Do not claim universal real-time capability.
- [x] Real-time wording must remain limited to tested video, hardware, resolution, and model configuration.

Recommended Phase 7 approach:

```text
Keep FPS Benchmark as the Phase 4 two-wheeler benchmark for now. Full pipeline benchmarking can be added later when the frame-level pipeline is consolidated.
```

## Forbidden in This Phase

- [x] Do not load `models/alpr.pt`.
- [x] Do not implement ALPR.
- [x] Do not implement EasyOCR.
- [x] Do not implement OCR fallback plate.
- [x] Do not implement tracking.
- [x] Do not assign track IDs.
- [x] Do not implement duplicate challan control.
- [x] Do not implement violation confirmation counters.
- [x] Do not generate PDF challans.
- [x] Do not save evidence images yet.
- [x] Do not send email.
- [x] Do not create SMS logs.
- [x] Do not add live camera input.
- [x] Do not treat `Unknown` helmet status as `No Helmet`.

## Acceptance Criteria

- [x] App runs using:

```bash
py -m streamlit run app.py
```

- [ ] User can upload a supported video.
- [x] Phase 2 metadata still displays correctly.
- [x] Phase 4 FPS benchmark remains available.
- [x] User can set two-wheeler confidence threshold.
- [x] User can set helmet confidence threshold.
- [x] User can set pose confidence threshold.
- [x] User can click Start Detection.
- [x] App loads `models/two-wheeler.pt`.
- [x] App loads `models/helmet-detection.pt`.
- [x] App loads `models/yolov8n-pose.pt`.
- [ ] App detects two-wheelers on the first readable frame when model/video support it.
- [x] App creates expanded bike+rider regions.
- [x] App runs helmet detection on expanded regions.
- [x] App runs pose inference once on the first frame.
- [x] App displays rider count per detected bike.
- [x] App marks triple riding when rider count is greater than or equal to 3.
- [x] App handles missing pose model file without crashing.
- [x] App handles zero pose detections as zero riders.
- [x] App handles frames with zero two-wheeler detections cleanly.
- [x] No ALPR, OCR, tracking, challan, email, or SMS code exists.

## Manual Test Plan

1. Confirm model files exist:

```powershell
Test-Path D:\codexWorkspace\Demo\models\two-wheeler.pt
Test-Path D:\codexWorkspace\Demo\models\helmet-detection.pt
Test-Path D:\codexWorkspace\Demo\models\yolov8n-pose.pt
```

2. Start the app:

```bash
py -m streamlit run app.py
```

3. Upload a valid traffic video.
4. Confirm metadata still displays.
5. Confirm the original first frame appears.
6. Adjust the two-wheeler confidence slider.
7. Adjust the helmet confidence slider.
8. Adjust the pose confidence slider.
9. Click Start Detection.
10. Confirm original bike boxes appear.
11. Confirm expanded bike+rider regions appear.
12. Confirm helmet status appears for each detected bike.
13. Confirm rider count appears for each detected bike.
14. Confirm triple-riding status appears only when rider count is at least 3.
15. Temporarily rename `models/yolov8n-pose.pt`.
16. Confirm missing-model error is shown cleanly.
17. Rename the model file back to `yolov8n-pose.pt`.

## Verification Commands

Run from:

```text
D:\codexWorkspace\Demo
```

Syntax check:

```powershell
@'
import ast
from pathlib import Path
for file_name in ["app.py", "src/config.py", "src/mock_database.py", "src/video_utils.py", "src/detector.py", "src/benchmark.py", "src/region_utils.py"]:
    ast.parse(Path(file_name).read_text(encoding="utf-8"), filename=file_name)
    print(f"syntax ok: {file_name}")
'@ | py -
```

Forbidden implementation scan:

```powershell
Select-String -Path app.py,src\*.py,requirements.txt -Pattern 'easyocr|reportlab|smtplib|twilio|pytesseract|paddleocr|alpr.pt|track_id|challan|sms|FastAPI|React|firebase|supabase|mongodb' -CaseSensitive:$false
```

Expected result:

```text
No forbidden later-phase implementation should appear, except explanatory UI text or existing phase-boundary documentation strings.
```

Allowed in this phase:

```text
ultralytics
YOLO
models/two-wheeler.pt
models/helmet-detection.pt
models/yolov8n-pose.pt
cv2
Helmet Present
No Helmet
Unknown
rider_count
triple_riding
```

## Completion Notes

Fill this after Phase 7 is implemented:

```text
Completed files:
app.py, README.md, src/config.py, src/detector.py, src/region_utils.py, notes/phase_07_checklist.md

Verification performed:
Confirmed `models/yolov8n-pose.pt`, `models/two-wheeler.pt`, and `models/helmet-detection.pt` exist with the required filenames. Python AST syntax validation passed for app.py, src/config.py, src/mock_database.py, src/video_utils.py, src/detector.py, src/benchmark.py, and src/region_utils.py. Loaded the pose model successfully; class names are `{0: 'person'}`. Ran pose inference on a generated RGB frame and verified zero-person output is handled cleanly. Verified rider association counts center-in-region and sufficient-keypoints-in-region cases. Forbidden later-phase implementation scan returned only explanatory UI text for ALPR/challans; no ALPR, OCR, tracking, PDF, email, or SMS implementation was added. Started Streamlit through a temporary PowerShell job and confirmed HTTP 200 from `http://127.0.0.1:8501`.

Known limitations:
Manual browser upload verification remains dependent on running Streamlit locally and selecting a real traffic video. Rider counting quality depends on the pose model's ability to detect people in the uploaded video frame and the expanded region covering the rider bodies. The current phase counts riders on the first readable frame only and does not confirm violations across multiple frames.

Next phase:
Phase 8 - ALPR Detection and OCR
```
