# How To Run The Demo On A New System

This file explains how to set up and run the two-wheeler traffic violation detection demo on another Windows computer.

## 1. What Should Be Inside The Project Folder

After unzipping, the folder should look like this:

```text
Demo/
  app.py
  requirements.txt
  readmeV1.md

  models/
    two-wheeler.pt
    helmet-detection.pt
    yolov8n-pose.pt
    alpr.pt
    easyocr/                   optional, if already downloaded

  .streamlit/
    config.toml

  run_app_cpu.bat
  run_app_gpu.bat
  restart_app_gpu.bat
  run_app_gpu_debug.bat
```

Optional model:

```text
models/two-wheeler-nano.pt
```

If this file is present, the app can use it as a smaller two-wheeler detector.

## 2. Install Python

Install Python 3.10 or newer from:

```text
https://www.python.org/downloads/
```

During installation, make sure this option is selected:

```text
Add Python to PATH
```

To check Python after installation, open Command Prompt and run:

```cmd
py --version
```

If Python is installed correctly, it will show a version number.

## 3. Open The Project Folder In Command Prompt

Example:

```cmd
cd /d D:\Demo
```

Use the actual path where the project was extracted.

For example, if the folder is on Desktop:

```cmd
cd /d C:\Users\YourName\Desktop\Demo
```

## 4. Create A Virtual Environment

Run:

```cmd
py -m venv .venv
```

This creates a local Python environment inside the project folder.

## 5. Activate The Virtual Environment

Run:

```cmd
.venv\Scripts\activate
```

After activation, the terminal should start with:

```text
(.venv)
```

Example:

```text
(.venv) D:\Demo>
```

## 6. Install Required Packages

Run:

```cmd
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

This may take several minutes.

## 7. Run The Demo On CPU

CPU mode works on most computers.

Run:

```cmd
python -m streamlit run app.py
```

Then open this link in a browser:

```text
http://localhost:8501
```

If the browser does not open automatically, copy and paste the link manually.

## 8. Run The Demo On NVIDIA GPU

Use this only if the system has an NVIDIA GPU.

First, check if NVIDIA is available:

```cmd
nvidia-smi
```

If this command shows GPU information, install CUDA-enabled PyTorch:

```cmd
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

Then check if PyTorch can use the GPU:

```cmd
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No CUDA')"
```

If it prints `True`, run the app:

```cmd
python -m streamlit run app.py
```

Inside the app, select:

```text
Inference device: GPU
```

If GPU does not work, use:

```text
Inference device: CPU
```

## 9. Easier Way To Start The App

After setup is complete, the user can start the app using the batch files.

For CPU:

```cmd
run_app_cpu.bat
```

For GPU:

```cmd
run_app_gpu.bat
```

If the app disconnects or an old server is stuck:

```cmd
restart_app_gpu.bat
```

For debugging:

```cmd
run_app_gpu_debug.bat
```

## 10. How To Use The App

1. Start the app.
2. Open:

```text
http://localhost:8501
```

3. Add mock owner details:
   - owner name
   - phone number
   - email address
4. Upload a traffic video.
5. Choose speed mode:
   - Best accuracy
   - Faster: process every 2nd frame
   - Faster: process every 3rd frame
   - Faster: process every 5th frame
6. Choose two-wheeler detector:
   - Current custom detector
   - Smaller COCO nano detector
7. Choose inference device:
   - Auto
   - GPU
   - CPU
8. Click:

```text
Process Video
```

9. After processing, the app shows:
   - processed video
   - FPS
   - total frames
   - time taken
   - violation table
   - generated challan download buttons

## 11. EasyOCR First Run

The first time OCR is used, EasyOCR may download model files.

The files are stored in:

```text
models/easyocr/
```

After the first successful download, it should not download again.

If `models/easyocr/` was included in the ZIP, this download may not be needed.

## 12. Output Files

The app creates an `outputs/` folder automatically.

Important output locations:

```text
outputs/processed_videos/   processed output videos
outputs/evidence/           violation evidence images
outputs/challans/           generated PDF challans
outputs/uploads/            uploaded videos
outputs/mock_owners.json    saved mock owner database
outputs/demo_sms_log.csv    demo SMS log
```

## 13. Common Problems And Fixes

### Problem: `streamlit` is not recognized

Use:

```cmd
python -m streamlit run app.py
```

instead of:

```cmd
streamlit run app.py
```

### Problem: GPU is not detected

Run:

```cmd
python -c "import torch; print(torch.cuda.is_available())"
```

If it prints `False`, use CPU mode or install CUDA-enabled PyTorch.

### Problem: No space left on device

Free disk space.

EasyOCR model files are stored in:

```text
models/easyocr/
```

Make sure the drive containing the project has enough space.

### Problem: Streamlit connection error

Close the browser tab and terminal.

Then run:

```cmd
restart_app_gpu.bat
```

Open:

```text
http://localhost:8501
```

### Problem: App is slow

Try:

```text
Speed mode: Faster: process every 2nd frame
```

or:

```text
Inference device: GPU
```

if GPU is available.

## 14. Important Note

This is an academic demo system.

It does not connect to a real government database.

Owner mapping is simulated using the mock owner details entered by the user.

Demo SMS is logged locally and is not actually sent through a telecom provider.
