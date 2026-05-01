# Model Details

## Required Model Files

```text
models/
+-- two-wheeler.pt
+-- helmet-detection.pt
+-- alpr.pt
`-- yolov8n-pose.pt
```

## Two-Wheeler Model

Path:

```text
models/two-wheeler.pt
```

Purpose:

- Detect two-wheelers or bikes in traffic frames.

Expected output:

- Bounding boxes around bikes.
- Confidence scores.
- Class label for bike/two-wheeler.

Usage:

- Run on full video frame.
- Output boxes are passed to tracking and region expansion.

## Helmet Detection Model

Path:

```text
models/helmet-detection.pt
```

Purpose:

- Detect helmet compliance in an expanded bike+rider region.

Expected classes may include:

- `With_Helmet`
- `Without_Helmet`

Helmet status mapping:

```text
With_Helmet detected       -> Helmet Present
Without_Helmet detected    -> No Helmet
Neither class detected     -> Unknown
```

Important:

- Do not run helmet detection only on the tight bike crop.
- Do not classify missing helmet detections as No Helmet.

## ALPR Detection Model

Path:

```text
models/alpr.pt
```

Purpose:

- Detect license plate region.

Expected class:

- Usually `license_plate`

Important:

- This YOLO `.pt` model most likely detects the plate region only.
- OCR is performed separately using EasyOCR.
- Seeing the number plate in the output image does not mean the model has read the plate text.

The correct architecture is:

```text
YOLO alpr.pt -> plate bounding box -> crop plate -> EasyOCR -> plate text
```

## Pose Model

Path:

```text
models/yolov8n-pose.pt
```

Purpose:

- Detect human pose keypoints.
- Support rider counting.

Source:

- Pretrained Ultralytics YOLOv8n pose model.

How to obtain:

```python
from ultralytics import YOLO

model = YOLO("yolov8n-pose.pt")
```

Ultralytics can download the model automatically on first use, or it can be downloaded manually from the official Ultralytics assets release and placed in `models/`.

Important:

- The pose model detects persons/keypoints.
- It does not directly know who is a rider.
- The system must associate detected persons with a bike using the expanded bike+rider region.

## Model Loading Rule

Models should be loaded once and reused. Do not reload YOLO models inside every frame loop.

Recommended loading location:

- `src/detector.py`

Example:

```python
from ultralytics import YOLO

two_wheeler_model = YOLO("models/two-wheeler.pt")
helmet_model = YOLO("models/helmet-detection.pt")
alpr_model = YOLO("models/alpr.pt")
pose_model = YOLO("models/yolov8n-pose.pt")
```


