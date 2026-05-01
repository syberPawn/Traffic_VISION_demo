# Notification Design

## Notification Types

The demo supports:

- Real email notification.
- Demo SMS log.

It does not support:

- Real SMS sending.
- WhatsApp messaging.
- Push notification.
- Government challan API.

## Email Notification

Email is sent when:

- A violation is confirmed.
- A PDF challan is generated.
- Email is enabled in the Streamlit UI.
- `.env` credentials are available.
- At least one owner email exists in the mock registry.

## Email Credentials

Credentials are stored in `.env`:

```text
EMAIL_SENDER=project_email@gmail.com
EMAIL_APP_PASSWORD=your_gmail_app_password
```

The app should load credentials using `python-dotenv`.

## Email Recipients

Recipients come from:

```text
data/mock_owner_registry.json
```

Because this is an academic demo without official database access, every registered demo email may receive the notification.

## Email Content

Email body should include:

- Owner name.
- Vehicle number or demo fallback number.
- OCR status.
- Violation type.
- Fine amount.
- Challan ID.
- Date and time.
- Academic demo disclaimer.

The generated PDF challan must be attached.

## Email Status

The system should record email status:

```text
Sent
Disabled
Failed: missing credentials
Failed: no recipients
Failed: SMTP error
```

Email status should appear in the Streamlit violation table.

## SMS Log

SMS is not actually sent.

For each registered phone number, the system logs:

```text
SMS sent to +91XXXXXXXXXX
```

Save logs to:

```text
outputs/sms_log.csv
```

Required columns:

```text
timestamp, challan_id, phone, message, status
```

## SMS Status

Possible statuses:

```text
Logged
Disabled
No registered phone numbers
Failed to write log
```

## Presentation Explanation

Use this explanation:

```text
The system sends real email because email can be configured safely using a project Gmail account and app password. Real SMS is not used because telecom APIs require registration, compliance steps, and internet delivery reliability. For the academic demo, SMS behavior is represented through a local log entry.
```


