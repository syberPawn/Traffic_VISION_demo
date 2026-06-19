# AI-Based Two-Wheeler Traffic Violation Detection Demo

This repository contains a local Streamlit demo for an academic two-wheeler traffic violation detection system.

The system processes an uploaded traffic video, detects two-wheelers, checks helmet and triple-riding violations, runs plate OCR only for violating vehicles, and generates demo challan records with evidence images.

The design is intentionally modular: the two-wheeler detector, helmet detector, pose estimator, ALPR model, OCR reader, mock owner registry, and challan generator are separate pieces so each part can be improved or replaced independently.

## Pipeline

1. Upload a traffic video.
2. Detect two-wheelers in each frame.
3. Expand the bike crop upward to include the rider and helmet area.
4. Run helmet detection on the expanded crop.
5. Run pose estimation and count riders associated with the bike.
6. Combine helmet status and rider count in the violation logic.
7. If a violation is detected, track that bike across later frames and keep the clearest/largest plate crop for OCR.
8. Generate one challan per violating track with timestamp, violation type, fine amount, evidence image, owner details, and demo SMS status.
9. Show the processed video, FPS summary, violation table, and challan PDFs in the app.

## Features

- Single-button video processing flow.
- Annotated output video preview inside the app.
- FPS, total frame count, and processing-time summary.
- Helmet violation detection.
- Triple-riding detection.
- ALPR and EasyOCR-based plate reading for violating vehicles.
- Multi-frame plate selection for vehicles that are initially far away.
- Duplicate challan prevention per tracked bike.
- Mock owner database for academic/demo assignment.
- PDF challan generation with evidence image.
- CPU and optional NVIDIA CUDA GPU execution.

## Project Structure

```text
.
+-- app.py                    # Main Streamlit application
+-- requirements.txt          # Python dependencies
+-- README.md                 # Project overview and setup guide
+-- readmeV1.md               # Extra Windows-focused run guide
+-- .env.example              # Optional email configuration template
+-- .gitignore                # Keeps local outputs, caches, and weights out of Git
+-- models/
|   +-- README.md             # Model weight instructions
|   `-- .gitkeep
+-- outputs/                  # Generated videos, evidence, challans, and logs
+-- docs/                     # Report/documentation assets
+-- notes/                    # Development phase notes
`-- src/
    `-- __init__.py
```

## What Not To Upload

These files are local runtime artifacts and should not be committed to GitHub:

- `.venv/`
- `.env`
- `models/*.pt`
- `models/easyocr/`
- `outputs/*`
- uploaded videos
- processed videos
- generated evidence images
- generated challan PDFs
- real owner/contact data such as `data/mock_owner_registry.json` or `outputs/mock_owners.json`
- private videos or real license plate data

## Required Model Files

Model weights are intentionally not committed. Place these files manually under `models/` before running the full system:

```text
models/
+-- two-wheeler.pt          # Custom two-wheeler detector
+-- helmet-detection.pt     # Helmet detector
+-- alpr.pt                 # Number plate detector
`-- yolov8n-pose.pt         # Pose estimation model
```

Optional smaller two-wheeler detector:

```text
models/two-wheeler-nano.pt
```

EasyOCR downloads its own OCR model files on first use and stores them in:

```text
models/easyocr/
```

That folder is ignored by Git so the OCR files are reused locally without being uploaded.

## Setup On A New Computer

Use Python 3.10 or newer. Python 3.11 or 3.12 is recommended.

1. Clone or download the repository.

```bash
git clone <your-repo-url>
cd Demo
```

2. Create a virtual environment.

```bash
py -m venv .venv
```

3. Activate the virtual environment.

```bash
.venv\Scripts\activate
```

4. Install dependencies.

```bash
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

5. Copy the required `.pt` model files into `models/`.

6. Start the app.

```bash
python -m streamlit run app.py
```

7. Open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Optional GPU Setup

The app can use CUDA when a compatible NVIDIA GPU, NVIDIA driver, and CUDA-enabled PyTorch installation are available.

Check whether PyTorch can see the GPU:

```bash
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No CUDA')"
```

If this prints `True` and the GPU name, select GPU mode in the app. If it prints `False`, the app still runs on CPU, but processing will be slower.

For CUDA installation, use the PyTorch command that matches your driver and CUDA version from the official PyTorch installation page. CUDA wheels can be several GB, so make sure the target drive has enough free space.

## Using The App

1. Add one or more demo vehicle owners in the owner section.
2. Upload a video.
3. Choose CPU or GPU mode.
4. Choose the two-wheeler detector option.
5. Click the process button.
6. Review the processed video, speed card, violation table, evidence images, and generated challans.

The owner mapping is a mock database for demonstration. If only one owner exists, all demo violations can be mapped to that owner. Local owner data is generated during app use and should not be uploaded to GitHub.

## Output Files

Generated files are written under `outputs/`:

```text
outputs/
+-- processed_videos/       # Annotated processed videos
+-- evidence/               # Evidence images used in challans
+-- challans/               # Generated PDF challans
+-- uploads/                # Temporary uploaded videos
+-- violation_log.csv       # Violation table export
`-- demo_sms_log.csv        # Demo SMS log
```

These outputs should not be committed to GitHub.

## Troubleshooting

If `streamlit` is not recognized, run it through Python:

```bash
python -m streamlit run app.py
```

If EasyOCR prints `Using CPU`, that message only refers to EasyOCR. The YOLO models can still use GPU if PyTorch CUDA is available and GPU mode is selected.

If you see `No space left on device`, clear temporary files, remove old generated outputs, or move the virtual environment/model cache to a drive with more free space.

If the app disconnects while processing a large video, try a shorter video, lower-resolution input, CPU/GPU setting changes, or clearing old files in `outputs/`.

## Academic Demo Disclaimer

This project is for academic demonstration and prototyping. It should not be used for real legal enforcement without validated datasets, stronger model evaluation, audit logging, security controls, privacy review, and human verification.
