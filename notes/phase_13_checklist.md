# Phase 13 Checklist - Email Notification

## Phase Goal

Send real email with PDF challan attached when email is explicitly enabled, Gmail credentials are available, a PDF challan is generated, and registered demo owner emails exist.

This phase must not send SMS and must not create SMS logs.

## Source Documents Read Before This Phase

- [x] `docs/03_development_phases.md`
- [x] `docs/08_notification_design.md`
- [x] `docs/10_streamlit_ui_design.md`
- [x] `notes/phase_12_checklist.md`

## Current Codebase State Before Phase 13

- [x] PDF challans are generated under `outputs/challans/`.
- [x] Registered owner emails are stored in `data/mock_owner_registry.json`.
- [x] `.env.example` contains `EMAIL_SENDER` and `EMAIL_APP_PASSWORD`.
- [x] Email is not implemented yet.

## Files to Create or Modify in Phase 13

- [x] Modify `requirements.txt`
- [x] Create `src/email_sender.py`
- [x] Modify `app.py`
- [x] Modify `README.md`
- [x] Update this checklist after implementation

## Email Requirements

- [x] Add `python-dotenv`.
- [x] Read `EMAIL_SENDER` and `EMAIL_APP_PASSWORD` from `.env`.
- [x] Use Gmail SMTP.
- [x] Send only when email is enabled in the UI.
- [x] Send only when a PDF challan exists.
- [x] Send to registered owner emails from `data/mock_owner_registry.json`.
- [x] Include owner name, vehicle/plate number, OCR status, violation type, fine amount, challan ID, date/time, and academic disclaimer.
- [x] Attach generated PDF challan.
- [x] Return and display email status.

## Email Status Requirements

- [x] `Sent`
- [x] `Disabled`
- [x] `Failed: missing credentials`
- [x] `Failed: no recipients`
- [x] `Failed: no PDF challan`
- [x] `Failed: SMTP error`

## Forbidden in This Phase

- [x] Do not send SMS.
- [x] Do not create `outputs/sms_log.csv`.
- [x] Do not use Twilio or any real SMS API.
- [x] Do not add live camera input.
- [x] Do not use a real database.

## Acceptance Criteria

- [x] App remains runnable.
- [x] Email toggle exists and defaults off.
- [x] Email disabled path records `Disabled`.
- [x] Missing credential path records `Failed: missing credentials`.
- [x] Missing recipients path records `Failed: no recipients`.
- [x] Email status appears in confirmed violation table and CSV.
- [x] No SMS workflow exists.

## Verification Commands

Run from:

```text
D:\codexWorkspace\Demo
```

Syntax check:

```powershell
@'
import ast
from pathlib import Path
for file_name in ["app.py", "src/email_sender.py"]:
    ast.parse(Path(file_name).read_text(encoding="utf-8"), filename=file_name)
    print(f"syntax ok: {file_name}")
'@ | py -
```

Forbidden implementation scan:

```powershell
Select-String -Path app.py,src\*.py,requirements.txt -Pattern 'twilio|sms_log|cv2.VideoCapture\(0\)' -CaseSensitive:$false
```

## Completion Notes

```text
Completed files:
app.py, README.md, requirements.txt, src/email_sender.py, notes/phase_13_checklist.md

Verification performed:
Python AST syntax validation passed for app.py and src/email_sender.py. Verified disabled email returns `Disabled`, enabled email without PDF returns `Failed: no PDF challan`, and enabled email with an existing PDF but no `.env` credentials returns `Failed: missing credentials`. Verified `python-dotenv` is installed. Forbidden scan found no Twilio, SMS log, or live camera implementation. Full app syntax validation passed and Streamlit responded with HTTP 200.

Known limitations:
No real email was sent during verification because `.env` credentials were not present. Real sending requires `EMAIL_SENDER` and `EMAIL_APP_PASSWORD` in a local untracked `.env` file and the UI email toggle enabled.

Next phase:
Phase 14 - Demo SMS Log
```
