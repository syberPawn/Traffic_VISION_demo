# Phase 4 Checklist - FPS Benchmark

## Phase Goal

Measure two-wheeler detection performance on the uploaded video and report whether the current model pipeline is real-time capable for the tested video, hardware, resolution, and model configuration.

This phase must not include helmet detection, rider counting, ALPR, OCR, tracking, violation logic, challan generation, email, or SMS.

## Source Documents Read Before This Phase

- [x] `docs/03_development_phases.md`
- [x] `docs/09_fps_benchmark.md`
- [x] `docs/10_streamlit_ui_design.md`
- [x] `docs/11_folder_structure.md`
- [x] `notes/phase_03_checklist.md`

## Files Created or Modified in Phase 4

- [x] Modify `app.py`
- [x] Modify `src/video_utils.py`
- [x] Create `src/benchmark.py`
- [x] Update `README.md`
- [x] Create this checklist

## Implementation Requirements

- [x] Reuse the Phase 3 two-wheeler detector.
- [x] Load the model once and reuse it.
- [x] Process every frame of the uploaded video.
- [x] Do not use frame skipping.
- [x] Do not save processed videos yet.
- [x] Do not add helmet, pose, ALPR, OCR, tracking, challan, email, or SMS code.

## Required Metrics

- [x] Input Video FPS.
- [x] Input Video Duration.
- [x] Total Frames Processed.
- [x] Total Processing Time.
- [x] System Processing FPS.
- [x] Average Time Per Frame.
- [x] Real-Time Factor.
- [x] Real-Time Capability Status.

## Acceptance Criteria

- [x] App starts using `py -m streamlit run app.py`.
- [ ] User can upload a supported video through the UI.
- [x] Phase 2 metadata display remains available.
- [x] Phase 3 first-frame detection remains available.
- [x] User can click Run FPS Benchmark.
- [x] App processes all frames without frame skipping.
- [x] App displays the required benchmark metrics.
- [x] App uses careful wording: real-time status applies only to the tested video, hardware, resolution, and model configuration.
- [x] No later-phase implementation exists.

## Verification Performed

```text
Completed files:
app.py, README.md, src/video_utils.py, src/benchmark.py, notes/phase_04_checklist.md

Verification performed:
Python AST syntax validation passed for app.py, src/config.py, src/mock_database.py, src/video_utils.py, src/detector.py, and src/benchmark.py. Forbidden later-phase implementation scan returned no matches in app.py, src/*.py, or requirements.txt. Ran the FPS benchmark directly against tmp/phase2_test.avi: metadata opened, 5 frames processed, system FPS/latency/real-time factor calculated, real-time status produced, and last annotated frame returned. Started Streamlit with `py -m streamlit run app.py --server.port 8501 --server.headless true` and confirmed HTTP 200 from `http://127.0.0.1:8501`.

Known limitations:
Manual browser upload verification remains dependent on an available local sample video selected through the Streamlit UI.

Next phase:
Phase 5 - Expanded Bike + Rider Region
```
