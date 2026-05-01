# Limitations and Future Work

## Current Limitations

### Uploaded Video Only

The first version supports uploaded video only. It does not use live CCTV or camera streaming.

Reason:

- Uploaded video is more stable for academic presentation.

Future work:

- Add webcam, IP camera, or Bluetooth camera support after the uploaded-video pipeline is complete.

### OCR Reliability

OCR may fail when plates are:

- Blurry.
- Too small.
- Overexposed.
- Underexposed.
- Tilted.
- Occluded.
- Non-standard.
- Captured at high speed.

Future work:

- Add super-resolution.
- Add perspective correction.
- Add dedicated Indian plate OCR model.
- Improve post-correction.

### Rider Counting Accuracy

Pose-based rider counting may struggle in:

- Heavy occlusion.
- Crowded traffic.
- Side-view ambiguity.
- Partial rider visibility.
- Nearby pedestrians overlapping the bike region.

Future work:

- Train a dedicated rider counting model.
- Improve bike-rider association.
- Use temporal smoothing across frames.

### Helmet Detection Ambiguity

Helmet detection may return Unknown when:

- Rider head is outside the crop.
- Rider is occluded.
- Helmet is visually similar to hair/cap.
- Image quality is poor.

Future work:

- Tune expanded region parameters.
- Train with more diverse helmet/no-helmet data.
- Add confidence calibration.

### Temporary Tracking

Simple IoU tracking can fail when:

- Bikes cross each other.
- Camera motion is high.
- Detections disappear for several frames.
- Occlusion happens.

Future work:

- Add ByteTrack, SORT, or DeepSORT if needed.
- Use plate number as secondary identity when OCR is stable.

### Mock Owner Registry

The demo does not connect to a real owner database.

Future work:

- Replace mock JSON registry with authorized database access in a real deployment.

### Demo SMS Only

SMS is not actually sent.

Future work:

- Integrate an approved SMS gateway only if registration and compliance requirements are available.

## Production Considerations

A production version would require:

- Legal approval.
- Secure database access.
- Auditable evidence storage.
- Tamper-resistant logs.
- Privacy controls.
- Model bias and accuracy evaluation.
- Human review workflow.
- Secure deployment.
- Robust camera integration.
- Official notification channels.

These are outside the academic demo scope.


