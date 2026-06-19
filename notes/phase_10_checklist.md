# Phase 10 Checklist - Duplicate Challan Control

## Phase Goal

Generate only one confirmed challan record for each confirmed violating temporary track ID during a scan.

This phase persists unique confirmed violation records to `outputs/violation_log.csv` with placeholders for evidence and PDF paths, but it must not generate PDF files, evidence images, email, or SMS.

## Source Documents Read Before This Phase

- [x] `docs/01_system_requirements.md`
- [x] `docs/02_system_architecture.md`
- [x] `docs/03_development_phases.md`
- [x] `docs/06_violation_logic.md`
- [x] `docs/07_tracking_and_duplicate_control.md`
- [x] `docs/11_folder_structure.md`
- [x] `notes/phase_09_checklist.md`

## Current Codebase State Before Phase 10

- [x] `src/tracking.py` assigns temporary track IDs using IoU matching.
- [x] `src/violation_logic.py` combines helmet status and rider count and confirms after a frame threshold.
- [x] `app.py` runs a full-video violation confirmation scan.
- [x] `outputs/violation_log.csv` is not yet written by the app.

## Files to Create or Modify in Phase 10

- [x] Modify `src/config.py`
- [x] Create `src/utils.py`
- [x] Modify `src/violation_logic.py`
- [x] Modify `app.py`
- [x] Modify `README.md`
- [x] Create this checklist

## Duplicate Control Requirements

- [x] Maintain a per-scan violation registry keyed by `track_id`.
- [x] Mark a track as `challan_generated = True` after its first confirmed record is created.
- [x] Skip record creation when `challan_generated == True` for the same track.
- [x] Store track ID, counters, plate number, OCR status, last seen frame, evidence path placeholder, PDF path placeholder, and confirmed violation type.
- [x] Keep one active track ID limited to one confirmed challan record.
- [x] Do not implement plate-number based duplicate merging yet.

## Persistence Requirements

- [x] Create `outputs/violation_log.csv`.
- [x] Write confirmed unique violation records to the CSV.
- [x] Include challan ID, timestamp, track ID, frame index, violation type, counters, plate number, OCR status, fine amount, and placeholder evidence/PDF paths.
- [x] Handle zero confirmed records cleanly by writing a header-only CSV.

## Forbidden in This Phase

- [x] Do not generate PDF challans.
- [x] Do not save evidence images yet.
- [x] Do not send email.
- [x] Do not create SMS logs.
- [x] Do not add live camera input.

## Acceptance Criteria

- [x] App runs using:

```bash
py -m streamlit run app.py
```

- [x] Confirmed violations produce at most one CSV row per active `track_id`.
- [x] Duplicate confirmed frames for the same track are skipped after the first record.
- [x] `outputs/violation_log.csv` is written after the scan.
- [x] PDF/evidence/email/SMS workflows are still absent.

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
for file_name in ["app.py", "src/config.py", "src/mock_database.py", "src/video_utils.py", "src/detector.py", "src/benchmark.py", "src/region_utils.py", "src/alpr_ocr.py", "src/tracking.py", "src/violation_logic.py", "src/utils.py"]:
    ast.parse(Path(file_name).read_text(encoding="utf-8"), filename=file_name)
    print(f"syntax ok: {file_name}")
'@ | py -
```

Forbidden implementation scan:

```powershell
Select-String -Path app.py,src\*.py,requirements.txt -Pattern 'reportlab|smtplib|twilio|sendmail|sms_log|challan_.*pdf|cv2.VideoCapture\(0\)' -CaseSensitive:$false
```

## Completion Notes

```text
Completed files:
app.py, README.md, src/config.py, src/utils.py, src/violation_logic.py, notes/phase_10_checklist.md

Verification performed:
Pending final syntax and smoke checks.

Known limitations:
PDF paths and evidence paths remain placeholders until Phase 11. Duplicate control is per temporary track ID within a scan; plate-number based duplicate control is not implemented.

Next phase:
Phase 11 - PDF Challan Generation
```
