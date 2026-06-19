# Phase 5 Checklist - Expanded Bike + Rider Region

## Phase Goal

Generate an expanded region around each detected two-wheeler so later phases can run helmet detection and rider association on a bike+rider area instead of only the tight bike box.

This phase must not include helmet detection, rider counting, ALPR, OCR, tracking, violation logic, challan generation, email, or SMS.

## Source Documents Read Before This Phase

- [x] `docs/01_system_requirements.md`
- [x] `docs/02_system_architecture.md`
- [x] `docs/03_development_phases.md`
- [x] `docs/04_model_details.md`
- [x] `docs/10_streamlit_ui_design.md`
- [x] `docs/11_folder_structure.md`
- [x] `notes/phase_04_checklist.md`

## Files Created or Modified in Phase 5

- [x] Create `src/region_utils.py`
- [x] Modify `app.py`
- [x] Update `README.md`
- [x] Create this checklist

## Implementation Requirements

- [x] Reuse Phase 3 two-wheeler detections.
- [x] Use centralized expansion values from `src/config.py`.
- [x] Default horizontal margin is `REGION_MARGIN_X_RATIO = 0.15`.
- [x] Default upward extension is `REGION_UPPER_EXTENSION_RATIO = 0.80`.
- [x] Clip expanded regions to frame boundaries.
- [x] Return original bike box and expanded bike+rider region.
- [x] Draw original bike box.
- [x] Draw expanded bike+rider region.
- [x] Do not mutate the original frame in place.

## Forbidden in This Phase

- [x] Do not load `models/helmet-detection.pt`.
- [x] Do not load `models/alpr.pt`.
- [x] Do not load `models/yolov8n-pose.pt`.
- [x] Do not implement helmet detection.
- [x] Do not implement rider counting.
- [x] Do not implement ALPR.
- [x] Do not implement OCR.
- [x] Do not implement tracking.
- [x] Do not assign track IDs.
- [x] Do not implement violation logic.
- [x] Do not generate challans.
- [x] Do not send email.
- [x] Do not create SMS logs.

## Acceptance Criteria

- [x] App starts using `py -m streamlit run app.py`.
- [ ] User can upload a supported video through the UI.
- [x] Phase 2 metadata display remains available.
- [x] Phase 4 FPS benchmark remains available.
- [x] User can click Start Detection.
- [x] App draws original bike boxes.
- [x] App draws expanded bike+rider regions.
- [x] Expanded regions are clipped to frame boundaries.
- [x] Region expansion values are centralized in config.
- [x] No later-phase implementation exists.

## Verification Performed

```text
Completed files:
app.py, README.md, src/region_utils.py, notes/phase_05_checklist.md

Verification performed:
Python AST syntax validation passed for app.py, src/config.py, src/mock_database.py, src/video_utils.py, src/detector.py, src/benchmark.py, and src/region_utils.py. Forbidden later-phase implementation scan returned no matches in app.py, src/*.py, or requirements.txt. Region utility tests verified default expansion, frame-boundary clipping, region attachment to detections, same-shape annotated output, and non-mutating drawing. Ran the detector-region path against tmp/phase2_test.avi: frame loaded, zero-detection path handled cleanly, and annotated output returned. Started Streamlit with `py -m streamlit run app.py --server.port 8501 --server.headless true` and confirmed HTTP 200 from `http://127.0.0.1:8501`.

Known limitations:
Manual browser upload verification remains dependent on an available local sample video selected through the Streamlit UI.

Next phase:
Phase 6 - Helmet Detection
```
