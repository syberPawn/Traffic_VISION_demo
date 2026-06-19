## Disclaimer

This system is built for academic and demonstration purposes only.

It is not intended for real legal enforcement without proper validation, authorization, compliance review, privacy safeguards, security controls, and human verification.

# AI-Based Two-Wheeler Traffic Violation Detection System

This repository contains a Streamlit-based computer vision system for detecting two-wheeler traffic violations from video input.

The system detects motorcycles or scooters, checks helmet usage, estimates rider count, performs number plate extraction for violating vehicles, and generates demo challan records with evidence images.

This project is developed as an academic prototype to demonstrate a modular AI-based traffic violation detection pipeline.

## Overview

The system processes an uploaded traffic video and identifies two major traffic violations:

- No helmet violation
- Triple riding violation

When a violation is detected, the system performs number plate detection and OCR on the violating vehicle. It then generates a demo challan containing the violation type, timestamp, fine amount, evidence image, mock owner details, and demo SMS status.

The system follows a modular architecture. Each major task is handled by a separate component, which makes it possible to replace or improve individual models without rebuilding the entire system.

## System Workflow

1. The user uploads a traffic video.
2. The two-wheeler detection model detects motorcycles or scooters in each frame.
3. The detected two-wheeler region is expanded upward to include the rider and helmet area.
4. The expanded crop is passed to the helmet detection model.
5. The pose estimation model is used to estimate the number of riders.
6. The violation logic checks whether the vehicle has:
   - No helmet violation
   - Triple riding violation
7. If a violation is detected, the same vehicle is tracked across later frames.
8. The system selects the clearest available number plate crop for OCR.
9. The ALPR model detects the number plate.
10. EasyOCR extracts the plate text.
11. A demo challan is generated with evidence and violation details.
12. The processed video, FPS information, violation table, and challan information are displayed in the Streamlit interface.

## Features

- Video upload through a Streamlit interface
- Two-wheeler detection
- Helmet detection using expanded bike crops
- Pose estimation for rider counting
- No helmet violation detection
- Triple riding violation detection
- Number plate detection using ALPR
- OCR using EasyOCR
- Multi-frame plate checking for improved OCR
- Duplicate challan prevention for the same tracked vehicle
- Mock owner database for demo purposes
- Demo SMS status logging
- PDF challan generation
- Evidence image generation
- Processed video playback with bounding boxes
- FPS, total frame count, and processing-time summary
- CPU and optional NVIDIA GPU support

## Project Structure

```text
.
+-- app.py
+-- requirements.txt
+-- README.md
+-- .env.example
+-- .gitignore
+-- .streamlit/
|   `-- config.toml
+-- models/
|   `-- README.md
+-- outputs/
|   +-- processed_videos/
|   +-- evidence/
|   +-- challans/
|   `-- uploads/
+-- notes/
`-- src/
```

## Model Files

The trained model files are provided separately through Google Drive.

Download the trained models from:

```text
https://drive.google.com/drive/folders/1hVIGVLaMPlA53bayK1qddneZHOPBK041?usp=sharing



Note- the files maybe named differently, both yolov8n-pose.pt and two-wheeler-nano.pt is not in the drive but it is available for download easily via ultralytics, visit - https://docs.ultralytics.com/models/yolov8#supported-tasks-and-modes.

```

After downloading, place the model files inside the `models/` folder.

Required model files:

```text
models/two-wheeler.pt
models/helmet-detection.pt
models/alpr.pt
models/yolov8n-pose.pt
```

Optional smaller two-wheeler model:

```text
models/two-wheeler-nano.pt (download it manually using ultralytics)
```

The expected model folder structure is:

```text
models/
+-- README.md
+-- two-wheeler.pt
+-- helmet-detection.pt
+-- alpr.pt
+-- yolov8n-pose.pt (manually download it)
`-- two-wheeler-nano.pt (manually download it)
```

EasyOCR downloads its own OCR model files during first use. These files are stored locally inside:

```text
models/easyocr/
```

## Requirements

The system requires Python 3.10 or newer.

Main dependencies:

- Streamlit
- OpenCV
- NumPy
- Pillow
- Ultralytics YOLO
- EasyOCR
- ReportLab
- Python Dotenv
- ImageIO
- ImageIO-FFmpeg

All required Python dependencies are listed in:

```text
requirements.txt
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
```

Create a virtual environment:

```bash
py -m venv .venv
```

Activate the virtual environment on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

Download the trained models from the provided Google Drive link and place them inside the `models/` folder.

## Running The Application

Start the Streamlit app:

```bash
python -m streamlit run app.py
```

After running the command, Streamlit will show a local URL in the terminal.

Usually, the app can be opened at:

```text
http://localhost:8501
```

## Using The System

1. Open the Streamlit app in the browser.
2. Add mock vehicle owner details.
3. Upload a traffic video.
4. Select CPU or GPU mode.
5. Select the two-wheeler detector option.
6. Click the process button.
7. Wait for the video to finish processing.
8. View the processed video with detection boxes.
9. Check the FPS, total frames, and processing-time summary.
10. Review detected violations in the violation table.
11. View the generated challan information and evidence.

## GPU Support

The system can run on CPU or GPU.

GPU mode requires:

- NVIDIA GPU
- Compatible NVIDIA driver
- CUDA-supported PyTorch installation

To check whether PyTorch can access the GPU, run:

```bash
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No CUDA')"
```

If the output shows `True` and displays the GPU name, GPU mode can be selected in the application.

If the output shows `False`, the system will run on CPU.

## Output Files

Generated output files are stored inside the `outputs/` folder.

```text
outputs/
+-- processed_videos/
+-- evidence/
+-- challans/
+-- uploads/
+-- violation_log.csv
`-- demo_sms_log.csv
```

Output folder usage:

- `processed_videos/` stores the annotated processed video.
- `evidence/` stores violation evidence images.
- `challans/` stores generated challan PDFs.
- `uploads/` stores uploaded video files during processing.
- `violation_log.csv` stores violation records.
- `demo_sms_log.csv` stores demo SMS log entries.

## Mock Owner Database

The system includes a mock owner database for demonstration purposes.

Owner details entered in the app are used to simulate how a traffic challan system could map detected violations to registered vehicle owners.

The mock owner database is only used for demonstration and does not connect to any real government or traffic authority database.

## Challan Generation

For each confirmed violation, the system generates challan information containing:

- Track ID
- Timestamp
- Frame number
- Violation type
- Fine amount
- Helmet status
- Rider count
- Plate result
- Mock owner name
- Mock owner phone number
- Mock owner email
- Demo SMS status
- Evidence image

The challan PDF includes the violation image, timestamp, violation type, and fine amount.

## Environment Variables

Email-related configuration can be added through a `.env` file when email functionality is enabled.

A sample environment file is provided:

```text
.env.example
```

Typical email configuration fields include:

```text
SMTP_HOST=
SMTP_PORT=
SMTP_USER=
SMTP_PASSWORD=
EMAIL_FROM=
```

## Notes

- This project is an academic prototype.
- Detection accuracy depends on the quality of the trained models.
- Helmet detection depends on crop quality, camera angle, lighting, and model performance.
- OCR accuracy depends on plate visibility, distance, blur, angle, and resolution.
- Processing speed depends on hardware, video resolution, model size, and CPU/GPU availability.
- The generated challans are for demonstration purposes only.
