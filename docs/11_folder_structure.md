# Folder Structure

## Recommended Structure

```text
two_wheeler_violation_demo/
|
+-- app.py
+-- requirements.txt
+-- README.md
+-- .env.example
+-- .gitignore
|
+-- docs/
|   +-- 00_project_overview.md
|   +-- 01_system_requirements.md
|   +-- 02_system_architecture.md
|   +-- 03_development_phases.md
|   +-- 04_model_details.md
|   +-- 05_alpr_and_ocr_design.md
|   +-- 06_violation_logic.md
|   +-- 07_tracking_and_duplicate_control.md
|   +-- 08_notification_design.md
|   +-- 09_fps_benchmark.md
|   +-- 10_streamlit_ui_design.md
|   +-- 11_folder_structure.md
|   +-- 12_demo_presentation_notes.md
|   `-- 13_limitations_and_future_work.md
|
+-- models/
|   +-- two-wheeler.pt
|   +-- helmet-detection.pt
|   +-- alpr.pt
|   `-- yolov8n-pose.pt
|
+-- data/
|   `-- mock_owner_registry.json
|
+-- src/
|   +-- config.py
|   +-- detector.py
|   +-- tracking.py
|   +-- region_utils.py
|   +-- violation_logic.py
|   +-- alpr_ocr.py
|   +-- challan_generator.py
|   +-- email_sender.py
|   +-- sms_logger.py
|   +-- mock_database.py
|   `-- utils.py
|
+-- outputs/
|   +-- challans/
|   +-- evidence/
|   +-- processed_videos/
|   +-- violation_log.csv
|   `-- sms_log.csv
|
`-- sample_videos/
    `-- demo_video.mp4
```

## File Responsibilities

### `app.py`

Streamlit entry point. It should coordinate UI and call functions from `src/`.

### `.env`

Local secrets file used at runtime. It should be created by the developer from `.env.example` and must not be committed.

### `.env.example`

Tracked template showing required environment variable names without real credentials.

### `src/config.py`

Central configuration:

- Paths.
- Model names.
- Threshold defaults.
- Fine amounts.
- Confirmation frame count.
- Region expansion ratios.
- Tracking thresholds.

### `src/detector.py`

YOLO model loading and inference wrappers:

- Two-wheeler detection.
- Helmet detection.
- ALPR detection.
- Pose inference.

### `src/tracking.py`

Temporary bike tracking:

- Track creation.
- IoU matching.
- Last seen frame update.
- Track cleanup.

### `src/region_utils.py`

Bounding box utilities:

- Expand bike region.
- Clip boxes.
- Crop frame regions.
- Compute IoU.

### `src/violation_logic.py`

Violation decision and confirmation:

- Helmet/rider rules.
- Violation counters.
- Confirmation threshold.
- Duplicate challan checks.

### `src/alpr_ocr.py`

License plate OCR:

- Plate crop preprocessing.
- EasyOCR calls.
- Text cleanup.
- Fallback demo plate rule.

### `src/challan_generator.py`

PDF generation:

- Create challan PDF.
- Add evidence image.
- Add disclaimer.

### `src/email_sender.py`

Email sending:

- Load `.env`.
- Build email.
- Attach PDF.
- Send through Gmail SMTP.

### `src/sms_logger.py`

Demo SMS logging:

- Write SMS log rows.
- Return SMS log status.

### `src/mock_database.py`

Mock owner registry:

- Read owners.
- Add owner.
- Validate owner fields.
- Save JSON.

### `src/utils.py`

Shared helpers:

- Timestamps.
- File naming.
- CSV append helpers.
- Safe directory creation.


