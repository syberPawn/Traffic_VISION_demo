# Model Files

Place local model weights in this folder before running the full demo.

Required files:

```text
two-wheeler.pt
helmet-detection.pt
alpr.pt
yolov8n-pose.pt
```

Optional file:

```text
two-wheeler-nano.pt
```

The `.pt` files are intentionally ignored by Git because model weights are large and may have licensing restrictions. Share them separately only if you have permission.

EasyOCR stores its downloaded OCR files in `models/easyocr/` on first use. That folder is also ignored by Git and does not need to be uploaded.
