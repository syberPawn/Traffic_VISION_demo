# Tracking and Duplicate Challan Control

## Problem

The same bike appears in many consecutive video frames. If the system generates a challan whenever a violation is detected in a frame, it will create duplicate challans for the same vehicle.

## Required Solution

Use temporary bike tracking and a violation registry.

Each detected bike receives a temporary track ID. The system stores violation evidence and counters against that track ID.

## Tracker Requirement

The first version must use simple IoU-based matching:

```text
If a new bike box overlaps sufficiently with an existing track box, assign the same track ID.
Otherwise, create a new track ID.
```

Default IoU threshold:

```text
0.3
```

Tracks inactive for a configurable number of frames should be removed.

Default inactive limit:

```text
30 frames
```

## Violation Registry Structure

Example:

```python
violation_registry = {
    4: {
        "track_id": 4,
        "no_helmet_count": 6,
        "triple_riding_count": 0,
        "combined_violation_count": 0,
        "plate_number": "MN01AB1234",
        "ocr_success": True,
        "challan_generated": True,
        "last_seen_frame": 125,
        "evidence_image_path": "outputs/evidence/challan_CH0001.jpg",
        "challan_pdf_path": "outputs/challans/challan_CH0001.pdf",
        "confirmed_violation_type": "No Helmet"
    }
}
```

## Duplicate Prevention Rule

```python
if violation_registry[track_id]["challan_generated"] is True:
    do_not_generate_another_challan()
```

One track ID can generate only one challan.

If the same physical bike leaves the frame and later re-enters with a new temporary track ID, the first version may treat it as a new track. Plate-number based duplicate prevention can be added later if OCR is stable enough.

## Evidence Selection

Evidence image should be saved when:

- Violation is confirmed.
- The frame clearly contains the bike and relevant detections.

Evidence should include annotations where possible:

- Bike box.
- Expanded region.
- Helmet status.
- Rider count.
- Plate box.
- Violation type.

## Plate Number and Tracking

Temporary bike tracking is not the same as official vehicle identity.

In the demo:

- Track ID prevents duplicate challans while the vehicle remains in the video.
- Plate number is used in the challan record.
- Mock owner registry does not perform real plate-to-owner lookup.

If OCR produces a stable plate number across frames later, it may be used as an additional duplicate key.


