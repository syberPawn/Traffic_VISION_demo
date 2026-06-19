# Phase 8 Checklist - ALPR Detection and OCR

## Phase Goal

Load `models/alpr.pt`, detect license plate regions for each bike-associated expanded region, crop the selected plate, and read text using EasyOCR.

This phase should display plate detection status, plate crop, OCR/fallback plate number, OCR confidence, and plate mode per detected bike.

This phase must not include tracking, violation confirmation, duplicate challan control, PDF generation, email, or SMS.

## Source Documents Read Before This Phase

- [x] `docs/01_system_requirements.md`
- [x] `docs/02_system_architecture.md`
- [x] `docs/03_development_phases.md`
- [x] `docs/04_model_details.md`
- [x] `docs/05_alpr_and_ocr_design.md`
- [x] `docs/10_streamlit_ui_design.md`
- [x] `docs/11_folder_structure.md`
- [x] `notes/phase_07_checklist.md`

## Required Model File

Before implementation, confirm this file exists:

```text
models/alpr.pt
```

Checklist:

- [x] `models/alpr.pt` exists.
- [x] Filename matches exactly: `alpr.pt`.
- [x] Do not rename code to fit a different model filename.
- [x] Keep using `models/two-wheeler.pt` for bike detection.
- [x] Keep using `models/helmet-detection.pt` for helmet status.
- [x] Keep using `models/yolov8n-pose.pt` for rider counting.

## Current Codebase State Before Phase 8

- [x] `app.py` coordinates Streamlit upload, metadata, first-frame detection, expanded regions, helmet detection, pose rider counting, FPS benchmark, and owner registry.
- [x] `src/detector.py` loads two-wheeler, helmet, and pose models.
- [x] `src/region_utils.py` creates clipped expanded bike+rider regions and draws bike, helmet, and rider labels.
- [x] `src/config.py` already contains `ALPR_CONFIDENCE = 0.25` and `DEMO_FALLBACK_PLATE = "DEMO-MN01-1234"`.
- [x] `README.md` currently marks ALPR and OCR as not included yet.

## Files to Create or Modify in Phase 8

- [x] Modify `requirements.txt`
- [x] Modify `src/config.py`
- [x] Modify `src/detector.py`
- [x] Create `src/alpr_ocr.py`
- [x] Modify `src/region_utils.py`
- [x] Modify `app.py`
- [x] Modify `README.md`
- [x] Update this checklist after implementation

Recommended config addition:

```python
ALPR_MODEL_PATH = MODELS_DIR / "alpr.pt"
```

## Dependency Changes

Add:

- [x] `easyocr`

Do not add:

- [x] `reportlab`
- [x] `python-dotenv`
- [x] email/SMS libraries
- [x] tracking libraries

Those belong to later phases.

## ALPR Detector Requirements

Add ALPR model support without breaking the existing detectors.

Required responsibilities:

- [x] Import Ultralytics YOLO only in `src/detector.py`.
- [x] Load `models/alpr.pt`.
- [x] Validate ALPR model file exists before loading.
- [x] Return a clear error if the ALPR model file is missing.
- [x] Load the ALPR model once per app run, not once per bike.
- [x] Run ALPR on the bike-associated region, not full frame, in this first implementation.
- [x] Filter plate detections by `ALPR_CONFIDENCE`.
- [x] Convert plate boxes from crop coordinates back to full-frame coordinates before drawing.
- [x] Select the highest-confidence plate when multiple plates are detected inside the bike-associated region.
- [x] Do not use full-frame plate detections for the current bike.
- [x] Do not decide violations.
- [x] Do not generate challans.
- [x] Do not create track IDs.

Recommended functions:

```python
load_alpr_model()
detect_license_plates(region_rgb, model, confidence_threshold: float) -> list[dict]
detect_license_plate_for_region(frame_rgb, expanded_region, model, confidence_threshold: float) -> dict
```

## OCR Requirements

Create OCR helpers in `src/alpr_ocr.py`.

- [x] Load EasyOCR reader once per app run.
- [x] Allow OCR to be disabled from the UI.
- [x] Run OCR only on selected plate crop.
- [x] Generate practical preprocessing variants:
  - [x] Original crop.
  - [x] Grayscale crop.
  - [x] Otsu thresholding.
  - [x] Adaptive Gaussian thresholding.
  - [x] CLAHE + Otsu.
  - [x] Inverted Otsu.
- [x] Clean OCR text by uppercasing, removing spaces/symbols, and keeping only `A-Z` and `0-9`.
- [x] Accept cleaned OCR text only when length is at least 6.
- [x] Select the acceptable OCR result with the highest confidence.
- [x] Use `DEMO-MN01-1234` only when OCR fails, plate crop is missing, OCR is disabled, or EasyOCR is unavailable.
- [x] Clearly mark fallback with `ocr_success = False` and `plate_mode = "Fallback demo number"`.
- [x] Clearly mark successful OCR with `ocr_success = True` and `plate_mode = "OCR"`.
- [x] Do not claim fallback is a real detected plate number.

Recommended result structure:

```python
{
    "plate_detected": True,
    "plate_box": [x1, y1, x2, y2],
    "plate_number": "MN01AB1234",
    "ocr_success": True,
    "ocr_confidence": 0.82,
    "plate_mode": "OCR",
    "ocr_raw_text": "MN 01 AB 1234"
}
```

## Streamlit UI Requirements

Update the app to include:

- [x] Sidebar ALPR confidence slider.
- [x] Sidebar OCR enabled/disabled checkbox.
- [x] Default ALPR confidence from `ALPR_CONFIDENCE`.
- [x] Start Detection should run:
  - [x] Two-wheeler detection.
  - [x] Expanded bike+rider region generation.
  - [x] Helmet detection on each expanded region.
  - [x] Pose inference once on the full first frame.
  - [x] Rider count association for each expanded region.
  - [x] ALPR on each expanded bike-associated region.
  - [x] OCR on each selected plate crop when OCR is enabled.
- [x] Show original bike boxes.
- [x] Show expanded bike+rider regions.
- [x] Show helmet status per detected two-wheeler.
- [x] Show rider count per detected two-wheeler.
- [x] Show plate box when detected.
- [x] Show plate number and plate mode per detected two-wheeler.
- [x] Show clear fallback status when OCR fails or is disabled.
- [x] Show clear error if `models/alpr.pt` is missing.
- [x] Keep FPS Benchmark available and unchanged.

## FPS Benchmark Boundary

Phase 4 FPS benchmark may remain a two-wheeler benchmark unless explicitly expanded.

- [x] Do not silently change benchmark meaning.
- [x] Do not include ALPR/OCR timing in the existing two-wheeler benchmark.
- [x] Do not claim universal real-time capability.
- [x] Real-time wording must remain limited to tested video, hardware, resolution, and model configuration.

## Forbidden in This Phase

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
- [x] Do not claim YOLO `alpr.pt` reads plate text by itself.
- [x] Do not claim OCR is active when OCR is disabled.

## Acceptance Criteria

- [x] App runs using:

```bash
py -m streamlit run app.py
```

- [x] User can upload a supported video.
- [x] Phase 2 metadata still displays correctly.
- [x] Phase 4 FPS benchmark remains available.
- [x] User can set two-wheeler confidence threshold.
- [x] User can set helmet confidence threshold.
- [x] User can set pose confidence threshold.
- [x] User can set ALPR confidence threshold.
- [x] User can enable or disable OCR.
- [x] User can click Start Detection.
- [x] App loads `models/two-wheeler.pt`.
- [x] App loads `models/helmet-detection.pt`.
- [x] App loads `models/yolov8n-pose.pt`.
- [x] App loads `models/alpr.pt`.
- [x] App runs ALPR on expanded bike-associated regions.
- [x] App displays plate box when detected.
- [x] App displays plate crop when detected.
- [x] App displays OCR plate number when OCR succeeds.
- [x] App displays fallback demo plate when OCR fails or is disabled.
- [x] App handles missing ALPR model file without crashing.
- [x] App handles missing EasyOCR dependency without crashing.
- [x] App handles zero plate detections cleanly.
- [x] No tracking, challan, PDF, email, or SMS code exists.

## Manual Test Plan

1. Confirm model files exist:

```powershell
Test-Path D:\codexWorkspace\Demo\models\two-wheeler.pt
Test-Path D:\codexWorkspace\Demo\models\helmet-detection.pt
Test-Path D:\codexWorkspace\Demo\models\yolov8n-pose.pt
Test-Path D:\codexWorkspace\Demo\models\alpr.pt
```

2. Start the app:

```bash
py -m streamlit run app.py
```

3. Upload a valid traffic video.
4. Confirm metadata still displays.
5. Confirm the original first frame appears.
6. Adjust all confidence sliders.
7. Toggle OCR enabled and disabled.
8. Click Start Detection.
9. Confirm original bike boxes and expanded regions appear.
10. Confirm helmet status and rider count still appear.
11. Confirm plate box appears when ALPR detects a plate.
12. Confirm plate number shows OCR or fallback mode clearly.
13. Temporarily rename `models/alpr.pt`.
14. Confirm missing-model error is shown cleanly.
15. Rename the model file back to `alpr.pt`.

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
for file_name in ["app.py", "src/config.py", "src/mock_database.py", "src/video_utils.py", "src/detector.py", "src/benchmark.py", "src/region_utils.py", "src/alpr_ocr.py"]:
    ast.parse(Path(file_name).read_text(encoding="utf-8"), filename=file_name)
    print(f"syntax ok: {file_name}")
'@ | py -
```

Forbidden implementation scan:

```powershell
Select-String -Path app.py,src\*.py,requirements.txt -Pattern 'reportlab|smtplib|twilio|track_id|challan|sms|FastAPI|React|firebase|supabase|mongodb|cv2.VideoCapture\(0\)' -CaseSensitive:$false
```

Expected result:

```text
No forbidden later-phase implementation should appear, except explanatory UI text or existing phase-boundary documentation strings.
```

Allowed in this phase:

```text
easyocr
models/alpr.pt
ALPR
OCR
plate_box
plate_crop
plate_number
ocr_success
plate_mode
Fallback demo number
```

## Completion Notes

Fill this after Phase 8 is implemented:

```text
Completed files:
requirements.txt, app.py, README.md, src/config.py, src/detector.py, src/alpr_ocr.py, src/region_utils.py, notes/phase_08_checklist.md

Verification performed:
Confirmed `models/alpr.pt`, `models/two-wheeler.pt`, `models/helmet-detection.pt`, and `models/yolov8n-pose.pt` exist with the required filenames. Python AST syntax validation passed for app.py, src/config.py, src/mock_database.py, src/video_utils.py, src/detector.py, src/benchmark.py, src/region_utils.py, and src/alpr_ocr.py. Loaded the ALPR model successfully; class names are `{0: 'license_plate'}`. Verified ALPR on a blank generated frame returns no plate cleanly. Verified OCR cleanup converts `MN-01 AB 1234` to `MN01AB1234`, accepts valid cleaned text length, and returns the clearly marked fallback demo plate when OCR is disabled or EasyOCR is unavailable. Forbidden later-phase implementation scan returned only explanatory UI text for challans; no tracking, PDF, email, or SMS implementation was added. Started Streamlit and confirmed HTTP 200 from `http://127.0.0.1:8501`.

Known limitations:
EasyOCR reader initialization is configured to use local `tmp/easyocr` storage and automatic downloads are disabled so the demo stays offline-friendly. If EasyOCR model files are not already present locally, OCR gracefully falls back to `DEMO-MN01-1234` with `plate_mode = "Fallback demo number"`. ALPR/OCR currently runs on the first readable frame only and does not confirm violations across multiple frames.

Next phase:
Phase 9 - Violation Decision Logic
```
