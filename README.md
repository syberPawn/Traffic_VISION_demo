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

Not included yet:

- YOLO inference.
- OCR.
- PDF challan generation.
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
