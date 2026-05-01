# Development Phases

## Development Rule

Build phase by phase. Do not implement the full system in one step. Each phase must leave the application runnable.

After each phase, provide:

- Completed checklist.
- Files created or modified.
- How to run.
- Known limitations.
- Next phase.

## Phase 1 - Streamlit Base App

Goal:

- Create basic Streamlit application and folder structure.
- Create a minimal mock owner registry form because it is needed for the base UI.

Acceptance:

- `streamlit run app.py` launches the app.
- User can upload a video file.
- UI shows title and description.
- Mock owner registry form exists.
- Saved owner list can be displayed.
- No YOLO inference.
- No PDF/email/SMS.

Boundary:

- Phase 1 only creates basic owner entry and display.
- Phase 12 later hardens validation and connects saved owners to email and SMS workflows.

## Phase 2 - Video Upload and Frame Reading

Goal:

- Read uploaded video using OpenCV.

Acceptance:

- Display input FPS.
- Display total frames.
- Display duration.
- Display resolution.
- Show video preview or first frame.
- No YOLO inference yet.

## Phase 3 - Two-Wheeler Detection

Goal:

- Load `models/two-wheeler.pt` and detect bikes.

Acceptance:

- Draw two-wheeler bounding boxes.
- Display annotated frame/output.
- Apply confidence threshold from UI.
- No helmet detection.
- No rider counting.
- No ALPR.
- No challan.

## Phase 4 - FPS Benchmark

Goal:

- Measure processing performance.

Acceptance:

- Show input video FPS.
- Show total frames processed.
- Show processing time.
- Show system FPS.
- Show average latency per frame.
- Show real-time factor.
- Show real-time capability status.

## Phase 5 - Expanded Bike + Rider Region

Goal:

- Generate expanded regions around each detected bike.

Acceptance:

- Draw original bike box.
- Draw expanded region.
- Region is clipped to frame boundaries.
- Expansion values are configurable or centralized.
- Default expansion uses 15% horizontal margin and 80% upward extension relative to bike box size.

## Phase 6 - Helmet Detection

Goal:

- Run `models/helmet-detection.pt` on expanded bike+rider region.

Acceptance:

- Classify helmet status as:
  - Helmet Present
  - No Helmet
  - Unknown
- Unknown is not treated as No Helmet.
- Display helmet status per bike.

## Phase 7 - Pose-Based Rider Counting

Goal:

- Load `models/yolov8n-pose.pt` and count riders associated with each bike.

Acceptance:

- Display rider count per bike.
- Count only persons/keypoints inside associated expanded region.
- Mark triple riding when rider count is greater than or equal to 3.
- Run pose inference once per frame by default, then associate people to each bike region.

## Phase 8 - ALPR Detection and OCR

Goal:

- Load `models/alpr.pt`, detect license plate region, crop the plate, and read text using EasyOCR.

Acceptance:

- Detect and draw plate bounding box.
- Save or display plate crop.
- Run ALPR on the bike-associated region in the first implementation.
- Run EasyOCR on plate crop.
- Clean OCR text by removing spaces/symbols and converting to uppercase.
- Use OCR result when valid.
- Use clearly marked fallback demo plate only when OCR fails or is disabled.
- Do not claim full plate recognition if OCR is disabled.

## Phase 9 - Violation Decision Logic

Goal:

- Combine helmet status and rider count.

Acceptance:

- Detect:
  - No Helmet
  - Triple Riding
  - No Helmet + Triple Riding
- Do not generate challan from a single frame.
- Maintain per-track violation counters.
- Confirm only after stability threshold is reached.

## Phase 10 - Duplicate Challan Control

Goal:

- Generate only one challan for each confirmed violating track ID.

Acceptance:

- Maintain violation registry.
- Skip challan generation if `challan_generated == True`.
- Store track ID, counters, plate number, evidence path, PDF path, and last seen frame.

## Phase 11 - PDF Challan Generation

Goal:

- Generate PDF challan for confirmed violation.

Acceptance:

- PDF includes:
  - Challan ID
  - Date/time
  - Vehicle ID / track ID
  - Plate number
  - OCR status
  - Violation type
  - Fine amount
  - Evidence image
  - Academic demo disclaimer

## Phase 12 - Mock Owner Registry

Goal:

- Harden and integrate the mock owner registry created in Phase 1.

Acceptance:

- Save data to `data/mock_owner_registry.json`.
- Display saved owners.
- Validate empty fields.
- Use registered owners for email and SMS demo log.
- Preserve the Phase 1 UI behavior while adding validation and integration.

## Phase 13 - Email Notification

Goal:

- Send real email with PDF challan attached.

Acceptance:

- Read credentials from `.env`.
- Use Gmail SMTP.
- Send to registered demo emails.
- Show email status in UI.
- Handle disabled email mode gracefully.

## Phase 14 - Demo SMS Log

Goal:

- Create SMS log entries for registered phone numbers.

Acceptance:

- Do not send real SMS.
- For each phone number, save:
  - timestamp
  - challan ID
  - phone number
  - message
  - status
- Display `SMS sent to +91XXXXXXXXXX` as demo status.

## Phase 15 - Final UI Polish

Goal:

- Make the demo presentable.

Acceptance:

- Clean Streamlit layout.
- Summary metric cards.
- Violation table.
- PDF download buttons.
- Status messages.
- Academic demo disclaimer.
- No architectural rule violations.


