# Demo Presentation Notes

## One-Minute Explanation

This project demonstrates an AI-based two-wheeler traffic violation detection system. The user uploads traffic video, and the system processes it frame by frame. It detects two-wheelers, checks helmet compliance, counts riders using pose estimation, detects and reads the license plate, confirms violations across multiple frames, prevents duplicate challans, generates a PDF challan, sends an email notification, logs a demo SMS, and reports processing FPS.

## Why Uploaded Video Is Used

Use this explanation:

```text
The research framework is suitable for roadside video or CCTV input. For the academic demo, uploaded video is used first because it is stable, repeatable, offline-friendly, and safer during presentation. Live camera input can be added later after the uploaded video pipeline is reliable.
```

## Why Mock Owner Registry Is Used

Use this explanation:

```text
Access to an official vehicle-owner database is not available for an academic project. Therefore, the demo uses a local mock owner registry where names, phone numbers, and email addresses are entered manually. In a real deployment, the detected license plate would be matched with an authorized transport database.
```

## Why Real SMS Is Not Used

Use this explanation:

```text
Real SMS is not used because telecom APIs require registration, compliance approval, sender ID setup, and internet delivery reliability. To keep the demo stable and presentation-safe, the system creates a local SMS log saying that an SMS was sent.
```

## Why Email Is Used

Use this explanation:

```text
Email is used because it can be configured safely through a project Gmail account and app password. The generated PDF challan is attached to the email to demonstrate how automated notification would work in a real enforcement workflow.
```

## How ALPR Works

Use this explanation:

```text
The ALPR model first detects the license plate region. The cropped plate image is then passed to EasyOCR to read the characters. If OCR fails due to blur, angle, or poor lighting, the system can use a clearly marked demo fallback plate number so that the challan workflow can still be demonstrated.
```

## How Real-Time Feasibility Is Claimed

Use this explanation:

```text
The system compares the input video FPS with the measured processing FPS. If the processing FPS is greater than or equal to the input FPS, the system is considered real-time capable for that tested video, hardware, resolution, and model configuration. The project does not claim that it is always real-time in every environment.
```

## Important Viva Points

- YOLO detects objects; EasyOCR reads plate text.
- Helmet Unknown is not treated as No Helmet.
- A challan is not generated from one frame.
- Tracking prevents duplicate challans.
- The owner registry is mocked because official database access is unavailable.
- SMS is logged, not actually sent.
- The system is modular, so each component can be improved independently.


