# Phase 12 Checklist - Mock Owner Registry

## Phase Goal

Harden and integrate the mock owner registry created in Phase 1.

This phase should validate owner entries, prevent duplicate demo owners, display saved owners, and expose registered owner emails/phones to the confirmed violation workflow for later email and SMS phases.

This phase must not send email and must not create SMS logs.

## Source Documents Read Before This Phase

- [x] `docs/03_development_phases.md`
- [x] `docs/08_notification_design.md`
- [x] `docs/10_streamlit_ui_design.md`
- [x] `docs/11_folder_structure.md`
- [x] `notes/phase_11_checklist.md`

## Current Codebase State Before Phase 12

- [x] `src/mock_database.py` reads and writes `data/mock_owner_registry.json`.
- [x] `app.py` has owner name, phone number, and email fields.
- [x] Empty fields are checked in the UI only.
- [x] Duplicate owners are not prevented yet.
- [x] Confirmed violation records do not include future notification recipient context yet.

## Files to Create or Modify in Phase 12

- [x] Modify `src/mock_database.py`
- [x] Modify `app.py`
- [x] Modify `README.md`
- [x] Update this checklist after implementation

## Registry Validation Requirements

- [x] Save owner data to `data/mock_owner_registry.json`.
- [x] Display saved owners.
- [x] Validate owner name is not empty.
- [x] Validate phone number is not empty.
- [x] Validate email address is not empty.
- [x] Validate email has a basic valid shape.
- [x] Validate phone number has a practical digit length.
- [x] Normalize saved email addresses.
- [x] Normalize saved phone numbers.
- [x] Prevent duplicate owners by email or phone number.
- [x] Preserve existing Phase 1 owner form behavior.

## Integration Requirements

- [x] Load registered owners during violation confirmation scan.
- [x] Add owner recipient summary fields to confirmed violation records.
- [x] Add owner email count and phone count for later notification phases.
- [x] Do not send email in this phase.
- [x] Do not write SMS logs in this phase.
- [x] Show a clear UI message when no owners are registered.

## Forbidden in This Phase

- [x] Do not use Gmail SMTP.
- [x] Do not read `.env` credentials.
- [x] Do not send email.
- [x] Do not create `outputs/sms_log.csv`.
- [x] Do not send real SMS.
- [x] Do not add cloud storage or a real database.

## Acceptance Criteria

- [x] App remains runnable.
- [x] User can save a valid owner.
- [x] Invalid owner input shows clear validation errors.
- [x] Duplicate email or phone is rejected.
- [x] Saved owners are displayed.
- [x] Confirmed violation records include registered owner recipient counts.
- [x] Email/SMS workflows remain unimplemented.

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
for file_name in ["app.py", "src/mock_database.py"]:
    ast.parse(Path(file_name).read_text(encoding="utf-8"), filename=file_name)
    print(f"syntax ok: {file_name}")
'@ | py -
```

Forbidden implementation scan:

```powershell
Select-String -Path app.py,src\*.py,requirements.txt -Pattern 'smtplib|sendmail|twilio|sms_log|EMAIL_APP_PASSWORD|EMAIL_SENDER' -CaseSensitive:$false
```

## Completion Notes

```text
Completed files:
app.py, README.md, src/mock_database.py, notes/phase_12_checklist.md

Verification performed:
Python AST syntax validation passed for app.py, src/mock_database.py, src/config.py, and src/violation_logic.py. Verified email normalization, phone normalization, validation errors for empty/invalid input, and owner notification summary counts. Forbidden implementation scan found no Gmail SMTP, `.env` credential reads, Twilio/SMS, or live camera code.

Known limitations:
Owner registry is still a local JSON file and does not perform real plate-to-owner lookup. Per docs, future email and SMS phases may notify all registered demo owners because this is an academic prototype without an official owner database.

Next phase:
Phase 13 - Email Notification
```
