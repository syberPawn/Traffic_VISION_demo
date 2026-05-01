# Violation Logic

## Inputs

For each tracked bike, the violation logic receives:

- Track ID.
- Helmet status.
- Rider count.
- Plate number.
- Plate/OCR status.
- Frame index.
- Evidence frame/crop.

## Helmet Status

Helmet status can only be one of:

```text
Helmet Present
No Helmet
Unknown
```

Mapping:

```text
With_Helmet detected       -> Helmet Present
Without_Helmet detected    -> No Helmet
No helmet-related detection -> Unknown
```

Mandatory rule:

```text
Unknown helmet status must not be treated as No Helmet.
```

## Rider Status

Rider count comes from pose-based person/keypoint association with the expanded bike+rider region.

Rules:

```text
rider_count < 3   -> No triple riding
rider_count >= 3  -> Triple riding
```

## Violation Type Decision

Decision table:

| Helmet Status | Rider Count | Violation Type |
|---|---:|---|
| No Helmet | >= 3 | No Helmet + Triple Riding |
| No Helmet | < 3 | No Helmet |
| Helmet Present | >= 3 | Triple Riding |
| Helmet Present | < 3 | No Violation |
| Unknown | >= 3 | Triple Riding |
| Unknown | < 3 | No Violation |

Reference logic:

```python
if helmet_status == "No Helmet" and rider_count >= 3:
    violation_type = "No Helmet + Triple Riding"
elif helmet_status == "No Helmet":
    violation_type = "No Helmet"
elif rider_count >= 3:
    violation_type = "Triple Riding"
else:
    violation_type = "No Violation"
```

## Stability Confirmation

Do not generate a challan from one frame.

Default threshold:

```text
same violation type appears for 5 frames for the same track ID
```

The threshold should be configurable in code, for example:

```python
VIOLATION_CONFIRMATION_FRAMES = 5
```

The frames do not need to be perfectly consecutive in the first implementation, but they must belong to the same active track ID. If a track disappears and is later recreated with a new track ID, it is treated as a new temporary vehicle identity unless a later phase adds plate-number based merging.

## Counters

Each track should maintain separate counters:

```python
{
    "no_helmet_count": 0,
    "triple_riding_count": 0,
    "combined_violation_count": 0
}
```

Counter update rule:

- Increment only the counter matching the current frame's violation.
- Do not increment any counter for `No Violation`.
- Combined violation should be counted separately from single violations.
- If the violation type changes for the same track, keep all counters but confirm only the first counter that reaches the threshold unless a challan has already been generated.

## Fine Amounts

Initial demo fine amounts may be:

```text
No Helmet: Rs. 1000
Triple Riding: Rs. 1000
No Helmet + Triple Riding: Rs. 2000
```

These are demo values unless verified against current local traffic rules. The PDF must mark them as academic demo amounts if not legally verified.


