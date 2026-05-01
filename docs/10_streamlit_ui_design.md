# Streamlit UI Design

## UI Goal

The Streamlit app should be a practical demo interface, not a marketing page. It should let the evaluator upload a video, configure thresholds, register demo owners, run detection, and inspect generated violation records.

## Required Sections

### 1. Project Header

Include:

- Project title.
- Short description.
- Academic prototype disclaimer.

Default title:

```text
AI-Based Two-Wheeler Traffic Violation Detection Demo
```

### 2. Sidebar Settings

Include:

- Video uploader.
- Two-wheeler confidence threshold.
- Helmet confidence threshold.
- ALPR confidence threshold.
- OCR enabled/disabled.
- Email enabled/disabled.
- SMS log enabled/disabled.
- Violation confirmation frame threshold.

### 3. Mock Owner Registry

Include fields:

- Owner name.
- Phone number.
- Email address.

Actions:

- Save owner.
- Clear form if needed.
- Display saved owners.

Storage:

```text
data/mock_owner_registry.json
```

### 4. Video Processing Panel

Include:

- Uploaded video preview or metadata.
- Start detection button.
- Current/annotated frame display.
- Progress indicator.
- Processing status messages.

### 5. Detection Summary Cards

Show:

- Total bikes detected.
- No-helmet violations.
- Triple-riding violations.
- Combined violations.
- Challans generated.

### 6. Performance Benchmark Panel

Show:

- Input FPS.
- System FPS.
- Average latency.
- Real-time factor.
- Real-time capability status.

### 7. Violation Table

Columns:

- Challan ID.
- Date/time.
- Track ID.
- Plate number.
- Plate mode/OCR status.
- Violation type.
- Fine amount.
- Email status.
- SMS log status.
- Evidence image path.
- PDF download button.

## UI Behavior Rules

- Do not show a challan row until violation is confirmed.
- Show OCR fallback status clearly.
- Show email errors without crashing the app.
- Show SMS as demo log only.
- Keep controls simple and presentation-safe.

## Initial Phase 1 UI

Phase 1 should only include:

- Project title.
- Short description.
- Sidebar.
- Video uploader.
- Owner registry form.
- Saved owner display.

Do not add detection, OCR, challan, email, or SMS in Phase 1.


