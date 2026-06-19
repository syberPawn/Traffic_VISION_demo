# Phase 6 Checklist - Helmet Detection

## Phase Goal

Load `models/helmet-detection.pt` using Ultralytics YOLO and run helmet detection on each expanded bike+rider region from Phase 5.

This phase should display helmet status per detected two-wheeler as one of:

- `Helmet Present`
- `No Helmet`
- `Unknown`

This phase must not include rider counting, ALPR, OCR, tracking, violation confirmation, duplicate challan control, PDF generation, email, or SMS.

## Source Documents Read Before This Phase

- [x] `docs/00_project_overview.md`
- [x] `docs/01_system_requirements.md`
- [x] `docs/02_system_architecture.md`
- [x] `docs/03_development_phases.md`
- [x] `docs/04_model_details.md`
- [x] `docs/06_violation_logic.md`
- [x] `docs/10_streamlit_ui_design.md`
- [x] `docs/11_folder_structure.md`
- [x] `docs/12_demo_presentation_notes.md`
- [x] `docs/13_limitations_and_future_work.md`
- [x] `notes/phase_05_checklist.md`

## Required Model File

Before implementation, confirm this file exists:

```text
models/helmet-detection.pt
```

Checklist:

- [x] `models/helmet-detection.pt` exists.
- [x] Filename matches exactly: `helmet-detection.pt`.
- [x] Do not rename code to fit a different model filename.
- [x] Do not load ALPR or pose models in this phase.
- [x] Keep using `models/two-wheeler.pt` for bike detection.

## Current Codebase State Before Phase 6

- [x] `app.py` coordinates Streamlit upload, metadata, first-frame detection, expanded regions, FPS benchmark, and owner registry.
- [x] `src/detector.py` currently loads and runs only the two-wheeler model.
- [x] `src/region_utils.py` creates clipped expanded bike+rider regions.
- [x] `src/benchmark.py` runs full-video two-wheeler FPS benchmarking only.
- [x] `src/video_utils.py` handles upload persistence, metadata, first-frame reads, and frame iteration.
- [x] `src/config.py` already contains `HELMET_CONFIDENCE = 0.35`.
- [x] `README.md` currently marks helmet detection as not included yet.

## Files to Create or Modify in Phase 6

- [x] Modify `src/config.py`
- [x] Modify `src/detector.py`
- [x] Modify `app.py`
- [x] Optional: modify `README.md`
- [x] Update this checklist after implementation

Recommended config addition:

```python
HELMET_MODEL_PATH = MODELS_DIR / "helmet-detection.pt"
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

## Helmet Detector Requirements

Add helmet model support without breaking the existing two-wheeler detector.

Required responsibilities:

- [x] Import Ultralytics YOLO only in `src/detector.py`.
- [x] Load `models/helmet-detection.pt`.
- [x] Validate helmet model file exists before loading.
- [x] Return a clear error if the helmet model file is missing.
- [x] Load the helmet model once per app run, not once per bike.
- [x] Run helmet inference on expanded bike+rider crops, not tight bike boxes.
- [x] Filter helmet detections by `HELMET_CONFIDENCE`.
- [x] Return helmet detections in crop coordinates and/or frame coordinates.
- [x] Classify each expanded region as `Helmet Present`, `No Helmet`, or `Unknown`.
- [x] Do not decide violations.
- [x] Do not generate challans.
- [x] Do not create track IDs.

Recommended functions:

```python
load_helmet_model()
detect_helmets(region_rgb, model, confidence_threshold: float) -> list[dict]
classify_helmet_status(helmet_detections: list[dict]) -> str
```

Optional helper if useful:

```python
detect_helmet_status_for_region(frame_rgb, expanded_region, model, confidence_threshold: float) -> dict
```

Recommended per-region result structure:

```python
{
    "helmet_status": "Helmet Present",
    "helmet_detections": [
        {
            "box": [x1, y1, x2, y2],
            "confidence": 0.88,
            "class_id": 0,
            "class_name": "With_Helmet"
        }
    ]
}
```

## Helmet Class Mapping Rules

Model class names may vary. Handle likely names defensively.

Helmet-present class examples:

- [x] `With_Helmet`
- [x] `with_helmet`
- [x] `helmet`
- [x] `Helmet`

No-helmet class examples:

- [x] `Without_Helmet`
- [x] `without_helmet`
- [x] `no_helmet`
- [x] `No Helmet`
- [x] `No_Helmet`

Required classification behavior:

- [x] If a no-helmet class is detected above threshold, status may be `No Helmet`.
- [x] If a helmet-present class is detected above threshold and no stronger no-helmet evidence exists, status may be `Helmet Present`.
- [x] If no helmet-related class is detected, status must be `Unknown`.
- [x] `Unknown` must never be treated as `No Helmet`.
- [x] Do not emit `No Violation` in this phase.
- [x] Do not combine helmet status with rider count in this phase.

Recommended conflict rule:

```text
If both helmet and no-helmet classes are detected in one expanded region, choose the highest-confidence helmet-related detection for the displayed status.
```

## Region and Coordinate Requirements

Helmet detection must use Phase 5 expanded regions.

- [x] Use `expanded_region` from `src/region_utils.py`.
- [x] Crop the expanded region from the RGB frame.
- [x] Do not run helmet detection on the whole frame by default.
- [x] Do not run helmet detection on the tight bike box.
- [x] Clip crop coordinates to frame boundaries.
- [x] Handle empty or invalid crops gracefully.
- [x] If drawing helmet boxes, convert crop coordinates back to full-frame coordinates before display.

## Streamlit UI Requirements

Update the app to include:

- [x] Sidebar helmet confidence slider.
- [x] Default slider value from `HELMET_CONFIDENCE`.
- [x] Start Detection should run:
  - [x] Two-wheeler detection.
  - [x] Expanded bike+rider region generation.
  - [x] Helmet detection on each expanded region.
- [x] Show original bike boxes.
- [x] Show expanded bike+rider regions.
- [x] Show helmet status per detected two-wheeler.
- [x] Show clear `Unknown` status when helmet detection is inconclusive.
- [x] Show clear error if `models/helmet-detection.pt` is missing.
- [x] Keep FPS Benchmark available.

Recommended display:

- [x] Bike box in green.
- [x] Expanded bike+rider region in orange.
- [x] Helmet status label near each expanded region.
- [x] Detection details JSON includes `helmet_status`.

## FPS Benchmark Boundary

Phase 4 FPS benchmark may remain a two-wheeler benchmark unless explicitly expanded.

- [x] Do not silently change benchmark meaning.
- [x] If helmet inference is added to the benchmark, label it clearly as a two-wheeler + helmet benchmark.
- [x] Do not claim universal real-time capability.
- [x] Real-time wording must remain limited to tested video, hardware, resolution, and model configuration.

Recommended Phase 6 approach:

```text
Keep FPS Benchmark as the Phase 4 two-wheeler benchmark for now. Helmet pipeline benchmarking can be added later when the frame-level pipeline is consolidated.
```

## Forbidden in This Phase

- [x] Do not load `models/alpr.pt`.
- [x] Do not load `models/yolov8n-pose.pt`.
- [x] Do not implement rider counting.
- [x] Do not classify triple riding.
- [x] Do not implement ALPR.
- [x] Do not implement EasyOCR.
- [x] Do not implement OCR fallback plate.
- [x] Do not implement tracking.
- [x] Do not assign track IDs.
- [x] Do not implement duplicate challan control.
- [x] Do not implement violation logic.
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
- [x] User can click Start Detection.
- [x] App loads `models/two-wheeler.pt`.
- [x] App loads `models/helmet-detection.pt`.
- [ ] App detects two-wheelers on the first readable frame.
- [x] App creates expanded bike+rider regions.
- [x] App runs helmet detection on expanded regions.
- [x] App displays helmet status per detected two-wheeler.
- [x] App handles missing helmet model file without crashing.
- [x] App handles zero helmet detections as `Unknown`.
- [x] App handles frames with zero two-wheeler detections cleanly.
- [x] No pose, ALPR, OCR, tracking, challan, email, or SMS code exists.

## Manual Test Plan

1. Confirm model files exist:

```powershell
Test-Path D:\codexWorkspace\Demo\models\two-wheeler.pt
Test-Path D:\codexWorkspace\Demo\models\helmet-detection.pt
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
8. Click Start Detection.
9. Confirm original bike boxes appear.
10. Confirm expanded bike+rider regions appear.
11. Confirm helmet status appears for each detected bike.
12. Try a high helmet confidence threshold.
13. Confirm inconclusive helmet regions show `Unknown`.
14. Temporarily rename `models/helmet-detection.pt`.
15. Confirm missing-model error is shown cleanly.
16. Rename the model file back to `helmet-detection.pt`.

## Verification Commands

Run from:

```text
D:\codexWorkspace\Demo
```

Syntax check:

```bash
py -m py_compile app.py src/config.py src/mock_database.py src/video_utils.py src/detector.py src/benchmark.py src/region_utils.py
```

If Windows pycache permissions block `py_compile`, use AST syntax validation:

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
Select-String -Path app.py,src\*.py,requirements.txt -Pattern 'easyocr|reportlab|smtplib|twilio|pytesseract|paddleocr|alpr.pt|yolov8n-pose|track_id|challan|sms|FastAPI|React|firebase|supabase|mongodb' -CaseSensitive:$false
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
models/helmet-detection.pt
cv2
Helmet Present
No Helmet
Unknown
```

## Completion Notes

Fill this after Phase 6 is implemented:

```text
Completed files:
app.py, README.md, src/config.py, src/detector.py, src/region_utils.py, notes/phase_06_checklist.md

Verification performed:
Confirmed `models/helmet-detection.pt` exists with the required filename. Python AST syntax validation passed for app.py, src/config.py, src/mock_database.py, src/video_utils.py, src/detector.py, src/benchmark.py, and src/region_utils.py. Forbidden later-phase implementation scan returned no matches in app.py, src/*.py, or requirements.txt. Loaded the helmet model successfully; class names are `{0: 'helmet', 1: 'without_helmet'}`. Verified helmet status classification maps no detections to `Unknown`, `helmet` to `Helmet Present`, and `without_helmet` to `No Helmet`. Ran helmet inference on a generated RGB crop and verified a status/detection result is returned. Verified missing helmet model path raises a clear FileNotFoundError. Ran the two-wheeler + expanded-region + helmet-status pipeline against tmp/phase2_test.avi; the zero-bike path handled cleanly and returned an annotated frame. Started Streamlit with `py -m streamlit run app.py --server.port 8501 --server.headless true` and confirmed HTTP 200 from `http://127.0.0.1:8501`.

Known limitations:
Manual browser upload verification remains dependent on an available local sample video selected through the Streamlit UI. The helmet checkpoint is an older YOLOv5-style file, so `src/detector.py` includes compatibility shims for its legacy module path, Windows `PosixPath` checkpoint entries, and older `fuse`/`forward` method signatures. The generated blank-crop test produced model detections, so final confidence behavior should be judged on real traffic frames rather than synthetic black images.

Next phase:
Phase 7 - Pose-Based Rider Counting
```
