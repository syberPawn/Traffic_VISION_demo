# Phase 9 Checklist - Violation Decision Logic

## Phase Goal

Combine helmet status and rider count into a violation type, maintain per-track violation counters, and confirm a violation only after the configured stability threshold is reached.

This phase should display confirmed violation records from a full-video scan, but it must not generate challans, PDFs, evidence images, email, or SMS.

## Source Documents Read Before This Phase

- [x] `docs/01_system_requirements.md`
- [x] `docs/02_system_architecture.md`
- [x] `docs/03_development_phases.md`
- [x] `docs/06_violation_logic.md`
- [x] `docs/07_tracking_and_duplicate_control.md`
- [x] `docs/10_streamlit_ui_design.md`
- [x] `docs/11_folder_structure.md`
- [x] `notes/phase_08_checklist.md`

## Current Codebase State Before Phase 9

- [x] `app.py` coordinates Streamlit upload, first-frame detection, helmet status, rider count, ALPR/OCR, FPS benchmark, and owner registry.
- [x] `src/detector.py` loads two-wheeler, helmet, pose, and ALPR models.
- [x] `src/alpr_ocr.py` handles EasyOCR/fallback plate text.
- [x] `src/region_utils.py` creates expanded bike+rider regions and draws annotations.
- [x] `src/config.py` contains `VIOLATION_CONFIRMATION_FRAMES = 5`, `TRACK_IOU_THRESHOLD = 0.30`, and `TRACK_MAX_MISSING_FRAMES = 30`.

## Files to Create or Modify in Phase 9

- [x] Create `src/tracking.py`
- [x] Create `src/violation_logic.py`
- [x] Modify `app.py`
- [x] Modify `src/region_utils.py`
- [x] Modify `README.md`
- [x] Update this checklist after implementation

## Tracking Boundary

Temporary tracking is required so violation counters are associated with the same bike across frames.

- [x] Implement simple IoU-based temporary bike tracking.
- [x] Assign a `track_id` to each detected bike.
- [x] Match detections to existing tracks when IoU is at least `TRACK_IOU_THRESHOLD`.
- [x] Remove stale tracks after `TRACK_MAX_MISSING_FRAMES`.
- [x] Do not implement duplicate challan control in this phase.
- [x] Do not persist a challan registry in this phase.

## Violation Logic Requirements

- [x] Implement the documented decision table:
  - [x] `No Helmet` + rider count `>= 3` -> `No Helmet + Triple Riding`
  - [x] `No Helmet` + rider count `< 3` -> `No Helmet`
  - [x] `Helmet Present` + rider count `>= 3` -> `Triple Riding`
  - [x] `Helmet Present` + rider count `< 3` -> `No Violation`
  - [x] `Unknown` + rider count `>= 3` -> `Triple Riding`
  - [x] `Unknown` + rider count `< 3` -> `No Violation`
- [x] Ensure `Unknown` helmet status is not treated as `No Helmet`.
- [x] Maintain separate counters per track:
  - [x] `no_helmet_count`
  - [x] `triple_riding_count`
  - [x] `combined_violation_count`
- [x] Increment only the counter matching the current frame's violation.
- [x] Do not increment counters for `No Violation`.
- [x] Confirm a violation only after the matching counter reaches `VIOLATION_CONFIRMATION_FRAMES`.
- [x] Do not generate a challan from a single-frame detection.
- [x] Do not generate PDFs, evidence images, email, or SMS.

## Streamlit UI Requirements

- [x] Add sidebar violation confirmation frame threshold control.
- [x] Keep existing upload, detection, OCR, and FPS benchmark UI.
- [x] Keep first-frame inspection available.
- [x] Add a full-video violation confirmation scan button.
- [x] Show scan progress.
- [x] Display confirmed violation records in a table.
- [x] Include track ID, frame index, plate number, plate mode/OCR status, helmet status, rider count, violation type, fine amount, and counter value.
- [x] Show clear message when no violations are confirmed.
- [x] Do not show PDF download buttons in this phase.

## Fine Amounts

Use academic demo amounts:

- [x] `No Helmet`: `1000`
- [x] `Triple Riding`: `1000`
- [x] `No Helmet + Triple Riding`: `2000`
- [x] Clearly keep these as demo values until PDF/legal verification phases.

## Forbidden in This Phase

- [x] Do not implement duplicate challan control.
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
- [x] User can configure violation confirmation frame threshold.
- [x] App assigns temporary track IDs during the full-video scan.
- [x] App combines helmet status and rider count into violation type.
- [x] App confirms only after threshold frames for the same track.
- [x] App displays confirmed violation records.
- [x] App does not generate a challan from one frame.
- [x] No PDF, evidence image, email, or SMS code exists.

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
for file_name in ["app.py", "src/config.py", "src/mock_database.py", "src/video_utils.py", "src/detector.py", "src/benchmark.py", "src/region_utils.py", "src/alpr_ocr.py", "src/tracking.py", "src/violation_logic.py"]:
    ast.parse(Path(file_name).read_text(encoding="utf-8"), filename=file_name)
    print(f"syntax ok: {file_name}")
'@ | py -
```

Forbidden implementation scan:

```powershell
Select-String -Path app.py,src\*.py,requirements.txt -Pattern 'reportlab|smtplib|twilio|sendmail|sms_log|challan_.*pdf|canvas|cv2.VideoCapture\(0\)' -CaseSensitive:$false
```

Expected result:

```text
No forbidden later-phase implementation should appear, except explanatory UI text or existing phase-boundary documentation strings.
```

## Completion Notes

```text
Completed files:
app.py, README.md, src/region_utils.py, src/tracking.py, src/violation_logic.py, notes/phase_09_checklist.md

Verification performed:
Python AST syntax validation passed for app.py, src/config.py, src/mock_database.py, src/video_utils.py, src/detector.py, src/benchmark.py, src/region_utils.py, src/alpr_ocr.py, src/tracking.py, and src/violation_logic.py. Verified the documented violation decision table, including Unknown + rider count behavior. Verified counter confirmation occurs only when the configured threshold is reached. Verified IoU tracking reuses track IDs for overlapping boxes and creates a new ID for distant boxes. Forbidden later-phase implementation scan returned no matches. Started Streamlit and confirmed HTTP 200 from `http://127.0.0.1:8501`.

Known limitations:
Manual browser upload verification remains dependent on selecting a real local traffic video. The confirmation scan runs the detection pipeline over the uploaded video and may be slow on CPU. Duplicate challan control is intentionally not implemented until Phase 10, and no PDF/evidence/email/SMS workflow exists yet.

Next phase:
Phase 10 - Duplicate Challan Control
```
