# System Requirements

## Locked Technology Stack

Language:

- Python

Frontend:

- Streamlit

Computer vision:

- OpenCV

Model inference:

- Ultralytics YOLO

OCR:

- EasyOCR

PDF generation:

- ReportLab

Email:

- Gmail SMTP
- Gmail App Password

Storage:

- Local JSON files
- Local CSV files

Execution:

- Local laptop
- VS Code

## Explicit Non-Requirements

Do not introduce these unless explicitly requested later:

- Real database.
- FastAPI backend.
- React frontend.
- Real SMS API.
- Live camera.
- Bluetooth camera.
- Cloud storage.
- Cloud-hosted inference.

## Input Requirement

Primary input mode:

- Uploaded video file through Streamlit.

Supported formats:

- `.mp4`
- `.avi`
- `.mov`
- `.mkv`

Live camera is not part of the first version. Uploaded video is preferred because it is stable, repeatable, offline-friendly, and safer for presentation.

## Model File Requirement

The application expects these model files:

```text
models/
+-- two-wheeler.pt
+-- helmet-detection.pt
+-- alpr.pt
`-- yolov8n-pose.pt
```

The model paths above are the locked paths for this demo. If the physical files have different names, rename the files to match the docs before implementation.

## Local Storage Requirement

The system must use local files only:

```text
data/mock_owner_registry.json
outputs/violation_log.csv
outputs/sms_log.csv
outputs/challans/
outputs/evidence/
outputs/processed_videos/
```

No SQL, MongoDB, Firebase, Supabase, cloud database, or external persistence layer should be added in the first version.

## Environment Variable Requirement

Email credentials must be read from `.env`:

```text
EMAIL_SENDER=project_email@gmail.com
EMAIL_APP_PASSWORD=your_gmail_app_password
```

The `.env` file must not be committed to version control.

The repository should contain `.env.example` with placeholder values, not real credentials.

## Safety and Correctness Rules

The following rules are mandatory:

- Helmet not detected must not be treated as no helmet.
- No challan should be generated from a single-frame detection.
- Violations must be confirmed across multiple frames.
- The same tracked bike must not generate duplicate challans.
- Real SMS must not be sent.
- Real email may be sent only when enabled in the UI and credentials are available.
- OCR failure must be handled gracefully with a clearly marked fallback value.
- Real-time capability must be claimed only for the tested video, hardware, and model configuration.

## Default Configuration Values

Use these defaults unless testing shows they must be tuned:

```text
TWO_WHEELER_CONFIDENCE = 0.35
HELMET_CONFIDENCE = 0.35
ALPR_CONFIDENCE = 0.25
POSE_CONFIDENCE = 0.25
VIOLATION_CONFIRMATION_FRAMES = 5
TRACK_IOU_THRESHOLD = 0.30
TRACK_MAX_MISSING_FRAMES = 30
REGION_MARGIN_X_RATIO = 0.15
REGION_UPPER_EXTENSION_RATIO = 0.80
DEMO_FALLBACK_PLATE = DEMO-MN01-1234
```

These values should live in `src/config.py`.


