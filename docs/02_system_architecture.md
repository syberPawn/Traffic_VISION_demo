# System Architecture

## High-Level Pipeline

```text
Uploaded Video
    v
Frame Extraction
    v
Two-Wheeler Detection
    v
Temporary Bike Tracking
    v
Expanded Bike + Rider Region
    v
Helmet Detection
    v
Pose-Based Rider Counting
    v
License Plate Detection
    v
EasyOCR Plate Text Reading
    v
Violation Decision Logic
    v
Multi-Frame Confirmation
    v
Duplicate Challan Control
    v
Evidence Image Saving
    v
PDF Challan Generation
    v
Email Notification
    v
Demo SMS Log
    v
Violation Table + FPS Benchmark
```

## Module Responsibilities

### Streamlit UI

Responsibilities:

- Accept video upload.
- Show project description and disclaimer.
- Provide sidebar settings.
- Allow owner registration.
- Start video processing.
- Display annotated frames.
- Display summary metrics.
- Display violation table.
- Provide PDF download buttons.

The UI must not contain business logic that belongs in `src/` modules.

### Video Reader

Responsibilities:

- Save uploaded video temporarily or into an output/input cache.
- Open video with OpenCV.
- Read FPS, frame count, duration, width, and height.
- Iterate through frames.
- Provide frames to detection pipeline.

### Two-Wheeler Detector

Responsibilities:

- Load `models/two-wheeler.pt`.
- Detect two-wheeler bounding boxes.
- Filter detections by confidence.
- Return boxes in frame coordinates.

This module only detects candidate bikes. It must not decide violations.

### Tracker

Responsibilities:

- Assign a temporary track ID to each detected two-wheeler.
- Maintain identity across nearby frames.
- Support duplicate challan prevention.

The first implementation must use simple IoU-based matching. It does not need a complex tracking library unless later required.

### Region Utility

Responsibilities:

- Expand bike bounding boxes upward and sideways.
- Clip expanded regions to frame boundaries.
- Return original bike region and expanded bike+rider region.

This is required because helmet detection on tight bike crops can miss rider heads.

Default expansion:

```text
margin_x = 15% of bike box width
upper_extension = 80% of bike box height
bottom = original bike box bottom
```

### Helmet Detector

Responsibilities:

- Load `models/helmet-detection.pt`.
- Run detection on expanded bike+rider regions.
- Identify helmet status:
  - Helmet Present
  - No Helmet
  - Unknown

Unknown must not be treated as No Helmet.

### Pose Rider Counter

Responsibilities:

- Load `models/yolov8n-pose.pt`.
- Detect persons and keypoints.
- Count only persons associated with the expanded bike+rider region.
- Return rider count per bike.

The pose model detects people, not bikes and not "riders" directly. Rider association is a system-level rule based on keypoints or person center inside the expanded bike+rider region.

Implementation decision:

- Run pose inference once on the full frame by default.
- For each bike, count only pose detections whose body center or sufficient keypoints fall inside that bike's expanded bike+rider region.
- Do not count all persons in the frame.

### ALPR and OCR Module

Responsibilities:

- Load `models/alpr.pt`.
- Detect license plate regions for the current tracked bike.
- Crop detected plate regions.
- Run EasyOCR on the crop.
- Clean OCR output.
- Return plate detection status, plate text, OCR confidence, and fallback status.

Important distinction:

- YOLO `alpr.pt` detects where the plate is.
- EasyOCR reads what text is written on the plate.

Implementation decision:

- Prefer running ALPR on the bike-associated region so plates from unrelated vehicles are not selected.
- Do not use full-frame ALPR for challan plate selection in the first implementation.
- If full-frame fallback is added later, the selected plate must still be associated back to the current bike region before use in a challan.

### Violation Logic

Responsibilities:

- Combine helmet status and rider count.
- Decide violation type.
- Maintain per-track counters for stable confirmation.
- Avoid single-frame challans.

### Challan Generator

Responsibilities:

- Generate PDF challan.
- Include challan ID, date/time, track ID, plate number, violation type, fine amount, evidence image, and academic disclaimer.
- Save PDF under `outputs/challans/`.

### Notification Modules

Email sender:

- Reads registered owners.
- Reads `.env` credentials.
- Sends real email with PDF attachment when enabled.
- Returns send status.

SMS logger:

- Does not send SMS.
- Writes demo log entries to `outputs/sms_log.csv`.

## Data Flow Contract

Each detected bike should produce a per-frame object similar to:

```python
{
    "frame_index": 125,
    "track_id": 4,
    "bike_box": [x1, y1, x2, y2],
    "expanded_region": [left, top, right, bottom],
    "helmet_status": "No Helmet",
    "rider_count": 3,
    "plate_detected": True,
    "plate_number": "MN01AB1234",
    "ocr_success": True,
    "violation_type": "No Helmet + Triple Riding"
}
```

Confirmed violation records should be persisted as rows in `outputs/violation_log.csv`.


