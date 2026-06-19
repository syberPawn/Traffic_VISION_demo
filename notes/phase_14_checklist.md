# Phase 14 Checklist - Demo SMS Log

## Phase Goal

Create local demo SMS log entries for registered phone numbers when a confirmed challan is generated.

This phase must not send real SMS.

## Source Documents Read Before This Phase

- [x] `docs/03_development_phases.md`
- [x] `docs/08_notification_design.md`
- [x] `notes/phase_13_checklist.md`

## Current Codebase State Before Phase 14

- [x] Confirmed violations generate records.
- [x] PDF challans are generated when ReportLab is available.
- [x] Email notification is optional and defaults off.
- [x] Registered owner phones are stored in `data/mock_owner_registry.json`.

## Files Created or Modified in Phase 14

- [x] Modify `src/config.py`
- [x] Create `src/sms_logger.py`
- [x] Modify `app.py`
- [x] Modify `README.md`
- [x] Create this checklist

## SMS Log Requirements

- [x] Add local SMS log path `outputs/sms_log.csv`.
- [x] Add demo SMS log toggle in the Streamlit sidebar.
- [x] Do not send real SMS.
- [x] Do not use Twilio or any SMS API.
- [x] Use registered phone numbers from the mock owner registry.
- [x] Format 10-digit demo phone numbers with `+91`.
- [x] Write required columns: `timestamp`, `challan_id`, `phone`, `message`, `status`.
- [x] Append log rows instead of overwriting previous SMS logs.
- [x] Add `sms_status` to confirmed violation records and CSV output.

## SMS Status Requirements

- [x] `Logged`
- [x] `Disabled`
- [x] `No registered phone numbers`
- [x] `Failed to write log`
- [x] Display `SMS sent to +91XXXXXXXXXX` as the demo status when rows are logged.

## Forbidden in This Phase

- [x] Do not send real SMS.
- [x] Do not add Twilio or telecom API dependencies.
- [x] Do not add live camera input.
- [x] Do not replace the local mock registry with a real database.

## Acceptance Criteria

- [x] App remains importable.
- [x] SMS logging is optional and defaults off.
- [x] Disabled SMS path records `Disabled`.
- [x] Missing phone path records `No registered phone numbers`.
- [x] Enabled path writes rows to `outputs/sms_log.csv`.
- [x] SMS status appears in confirmed violation table and violation CSV.

## Verification Performed

```text
Python AST syntax validation passed for app.py and every src/*.py file.
Verified disabled SMS logging returns Disabled.
Verified enabled SMS logging with no registered phones returns No registered phone numbers.
Verified enabled SMS logging with a registered phone writes a local CSV row with status Logged.
Verified 10-digit phone formatting displays SMS sent to +91XXXXXXXXXX.
Forbidden implementation scan found no Twilio, real SMS client, send_sms implementation, or live camera code.
App and src.sms_logger import checks passed.
```

## Known Limitations

```text
SMS is represented only as a local CSV log for academic demo purposes. No telecom provider is contacted.
```

## Next Phase

```text
Phase 15 - Final UI Polish
```
