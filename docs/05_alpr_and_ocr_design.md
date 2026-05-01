# ALPR and OCR Design

## Core Clarification

ALPR in the full system has two separate parts:

1. License plate detection.
2. License plate text recognition.

In this demo:

- `models/alpr.pt` performs license plate detection.
- EasyOCR performs text recognition.

The YOLO model and OCR engine must not be described as the same thing.

## Plate Detection

Input:

- Bike-associated crop or expanded bike+rider region.

Model:

```text
models/alpr.pt
```

Output:

- Plate bounding box.
- Detection confidence.
- Plate crop.

The detected plate crop should be clipped safely to frame boundaries before OCR.

Selection rule:

- The plate used for a challan must belong to the current tracked bike.
- Do not use a plate detected elsewhere in the frame for the current bike.
- If multiple plates are detected in the bike-associated region, choose the highest-confidence plate box or the one best contained by the bike region.

## OCR Pipeline

Input:

- Cropped plate image.

OCR engine:

- EasyOCR.

Basic flow:

```text
Plate crop
    v
Preprocessing variants
    v
EasyOCR on each variant
    v
Select best result
    v
Clean text
    v
Validate length/format
    v
Return plate number
```

## Recommended Preprocessing Variants

The ANPR paper uses a multi-strategy EasyOCR approach. The demo should implement a practical version:

- Original crop.
- Grayscale crop.
- Otsu thresholding.
- Adaptive Gaussian thresholding.
- CLAHE + Otsu.
- Inverted Otsu.

The OCR result with the highest confidence and acceptable text length should be selected.

## OCR Text Cleanup

OCR output should be cleaned before use:

```text
1. Convert to uppercase.
2. Remove spaces.
3. Remove punctuation and symbols.
4. Keep only A-Z and 0-9.
```

Example:

```text
"MN 01 AB 1234" -> "MN01AB1234"
"MN-01-AB-1234" -> "MN01AB1234"
```

## Basic Validation

Minimum rule:

- Accept cleaned OCR text only if length is at least 6 characters.

Better rule:

- Prefer plate-like strings with letters and digits.
- Apply Indian plate format correction where possible.

## Indian Plate Post-Correction

Indian number plates commonly follow:

```text
[State Code][District Number][Series][Registration Number]
```

Example:

```text
MN01AB1234
AS03XY5678
```

Common OCR confusions:

```text
O <-> 0
I <-> 1
Q <-> 0
S <-> 5
B <-> 8
Z <-> 2
```

Position-aware correction may be added:

- State code positions should be letters.
- District positions should be digits.
- Series positions should be letters.
- Final registration positions should be digits.

This correction should be conservative. Do not over-correct uncertain OCR into a fake valid number.

## Fallback Rule

If OCR fails:

```text
plate_number = "DEMO-MN01-1234"
ocr_success = False
plate_mode = "Fallback demo number"
```

If OCR succeeds:

```text
plate_number = detected OCR text
ocr_success = True
plate_mode = "OCR"
```

The UI and PDF challan should clearly show whether the plate number came from OCR or fallback.

## What Must Not Be Claimed

Do not claim:

- The YOLO `.pt` model reads plate text by itself.
- The demo has full OCR when EasyOCR is disabled.
- A fallback demo plate is a real detected plate number.

Correct claim:

```text
The ALPR module detects the plate region using YOLO. The plate crop is then passed to EasyOCR for text recognition. If OCR fails, a clearly marked demo fallback plate is used to complete the academic challan workflow.
```


