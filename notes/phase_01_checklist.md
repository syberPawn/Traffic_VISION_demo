# Phase 1 Checklist - Streamlit Base App

## Phase Goal

Create the initial Streamlit application and base project structure.

This phase must not include YOLO inference, OpenCV video processing, PDF generation, email sending, or SMS logging.

## Files and Folders to Create

- [x] app.py
- [x] requirements.txt
- [x] README.md
- [x] .gitignore
- [x] .env.example
- [x] models/
- [x] data/
- [x] src/
- [x] outputs/
- [x] outputs/challans/
- [x] outputs/evidence/
- [x] outputs/processed_videos/
- [x] sample_videos/
- [x] data/mock_owner_registry.json

## Required Initial JSON

Create:

```text
data/mock_owner_registry.json
```

With:

```json
{
  "owners": []
}
```

## Streamlit UI Requirements

- [x] Show project title.
- [x] Show short academic demo description.
- [x] Show academic prototype disclaimer.
- [x] Add sidebar.
- [x] Add video uploader in sidebar.
- [x] Accept `.mp4`, `.avi`, `.mov`, `.mkv`.
- [x] Add mock owner registry form.
- [ ] Owner form fields:
  - [x] Owner name
  - [x] Phone number
  - [x] Email address
- [x] Add save owner button.
- [x] Display saved owners.
- [x] Show uploaded video filename when a video is uploaded.
- [x] Do not process video yet.

## Forbidden in This Phase

- [x] Do not load YOLO models.
- [x] Do not import Ultralytics.
- [x] Do not run OpenCV frame extraction.
- [x] Do not generate PDF.
- [x] Do not send email.
- [x] Do not create SMS log.
- [x] Do not implement detection logic.
- [x] Do not implement tracking.
- [x] Do not implement OCR.

## Acceptance Criteria

- [ ] App runs using:

```bash
streamlit run app.py
```

- [ ] User can upload a video file.
- [x] User can add demo owner details.
- [x] Owner details are saved to `data/mock_owner_registry.json`.
- [x] Saved owners are displayed in the UI.
- [x] App remains simple and stable.
- [x] No detection or notification functionality exists yet.

## Manual Test Plan

1. Start the app:

```bash
streamlit run app.py
```

2. Confirm the page loads.
3. Upload a sample video.
4. Confirm the uploaded filename appears.
5. Add a demo owner.
6. Confirm the owner appears in the saved owner list.
7. Open `data/mock_owner_registry.json`.
8. Confirm the owner was saved correctly.

## Completion Notes

Fill this after Phase 1 is implemented:

```text
Completed files:
app.py, requirements.txt, README.md, .gitignore, .env.example, data/mock_owner_registry.json, src/__init__.py, and required Phase 1 folders.

Known limitations:
Streamlit is not installed in the current Python environment. `py -m pip install -r requirements.txt` could not find the package from the configured package source, so the Streamlit runtime launch could not be verified here. The app syntax and registry helper behavior were verified.

Next phase:
Phase 2 - Video Upload and Frame Reading
```
