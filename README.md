# AI-Based Two-Wheeler Traffic Violation Detection Demo

Local Streamlit demo for an academic two-wheeler traffic violation detection system.

## Current Phase

Current scope:

- Base Streamlit app.
- Uploaded video UI.
- Local mock owner registry.
- Required project folders.
- OpenCV video metadata reading.
- Uploaded video preview.
- First-frame preview.
- Two-wheeler confidence threshold.
- First-frame two-wheeler detection using `models/two-wheeler.pt`.
- Annotated two-wheeler bounding-box display.
- Full-video FPS benchmark for the two-wheeler detection stage.
- Real-time capability status for the tested video and hardware.

Not included yet:

- Helmet detection.
- Rider counting.
- ALPR.
- OCR.
- PDF generation.
- Email notification.
- SMS logging.

## Run

Install dependencies:

```bash
py -m pip install -r requirements.txt
```

Start the app:

```bash
streamlit run app.py
```

Run the command from the project root:

```text
D:\codexWorkspace\Demo
```

## Model Files

Model weights are intentionally not committed to Git. Place them locally under:

```text
models/
+-- two-wheeler.pt
+-- helmet-detection.pt
+-- alpr.pt
`-- yolov8n-pose.pt
```
