# AI-Based Two-Wheeler Traffic Violation Detection Demo

## Purpose

This project is a local academic prototype for demonstrating an AI-based two-wheeler traffic violation detection system. It is based on the research framework that combines two-wheeler detection, helmet compliance detection, rider counting, license plate detection, OCR-based plate reading, violation aggregation, and challan generation.

The demo is designed for final-year project presentation, experimentation, and explanation. It is not a production traffic enforcement system.

## Primary Goal

Build a Streamlit application that allows a user to upload a traffic video and process it frame by frame to detect two-wheeler traffic violations.

The system should identify:

- No Helmet
- Triple Riding
- No Helmet + Triple Riding

For confirmed violations, the system should:

- Save evidence image locally.
- Detect the license plate region.
- Read plate text using EasyOCR, with a clearly marked demo fallback only if OCR fails or is disabled.
- Generate a PDF challan.
- Send a real email notification with the challan attached.
- Create a demo SMS log entry.
- Show violation results in the Streamlit UI.
- Show FPS benchmark metrics for real-time feasibility on the tested hardware and video.

## Research Alignment

The research paper proposes a modular AI framework with these stages:

1. Frame acquisition and preprocessing.
2. Two-wheeler detection.
3. Helmet detection.
4. Rider counting using YOLOv8 pose estimation.
5. License plate detection and text recognition.
6. Violation aggregation.
7. Challan or violation record generation.

This demo follows the same architecture, with presentation-safe implementation choices:

- Uploaded video is used instead of live CCTV in the first version.
- Local JSON and CSV files are used instead of a real database.
- A mock owner registry is used instead of official transport records.
- Real email notification is used.
- SMS is logged as a demo entry only.

## Scope

Included in the first complete demo:

- Streamlit frontend.
- Uploaded video input.
- OpenCV frame extraction.
- Ultralytics YOLO inference.
- Two-wheeler detection.
- Expanded bike+rider region generation.
- Helmet detection on expanded region.
- YOLOv8n-pose based rider counting.
- ALPR model based license plate region detection.
- EasyOCR based plate text reading.
- Violation decision logic.
- Multi-frame confirmation.
- Temporary bike tracking.
- Duplicate challan prevention.
- PDF challan generation.
- Mock owner registry.
- Real email notification.
- Demo SMS log.
- FPS benchmark.

Excluded from the first version:

- Live camera input.
- Bluetooth camera input.
- Real database.
- Official vehicle-owner lookup.
- Real SMS API.
- React frontend.
- FastAPI backend.
- Cloud deployment.
- Production authentication.

## Non-Production Disclaimer

This project is an academic prototype. The generated challans, SMS logs, owner registry, and vehicle-owner mapping are for demonstration only. In a real deployment, the license plate number would be matched against an authorized government transport database, and notifications would be sent through approved enforcement channels.


