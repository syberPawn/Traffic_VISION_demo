from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import cv2

from src.config import TWO_WHEELER_MODEL_PATH


def _clamp_confidence_threshold(confidence_threshold: float) -> float:
    return min(max(float(confidence_threshold), 0.0), 1.0)


def _clip_box_to_frame(
    box_values: list[float],
    frame_width: int,
    frame_height: int,
) -> list[int] | None:
    x1, y1, x2, y2 = [int(round(value)) for value in box_values]
    x1 = min(max(x1, 0), frame_width - 1)
    y1 = min(max(y1, 0), frame_height - 1)
    x2 = min(max(x2, 0), frame_width - 1)
    y2 = min(max(y2, 0), frame_height - 1)

    if x2 <= x1 or y2 <= y1:
        return None

    return [x1, y1, x2, y2]


def load_two_wheeler_model(model_path: Path = TWO_WHEELER_MODEL_PATH) -> Any:
    """Load the two-wheeler YOLO model after validating the local weight file."""
    if not model_path.exists():
        raise FileNotFoundError(
            f"Two-wheeler model file not found: {model_path}. "
            "Place the model at models/two-wheeler.pt."
        )

    yolo_config_dir = Path("tmp") / "ultralytics"
    yolo_config_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("YOLO_CONFIG_DIR", str(yolo_config_dir))

    from ultralytics import YOLO

    return YOLO(str(model_path))


def detect_two_wheelers(
    frame_rgb_or_bgr: Any,
    model: Any,
    confidence_threshold: float,
) -> list[dict[str, object]]:
    confidence_threshold = _clamp_confidence_threshold(confidence_threshold)
    results = model.predict(frame_rgb_or_bgr, conf=confidence_threshold, verbose=False)
    if not results:
        return []

    result = results[0]
    boxes = getattr(result, "boxes", None)
    if boxes is None:
        return []

    names = getattr(result, "names", {}) or getattr(model, "names", {}) or {}
    detections: list[dict[str, object]] = []
    frame_height, frame_width = frame_rgb_or_bgr.shape[:2]

    for box in boxes:
        confidence = float(box.conf[0])
        if confidence < confidence_threshold:
            continue

        class_id = int(box.cls[0])
        class_name = str(names.get(class_id, f"class_{class_id}"))
        clipped_box = _clip_box_to_frame(
            box.xyxy[0].tolist(),
            frame_width=frame_width,
            frame_height=frame_height,
        )
        if clipped_box is None:
            continue

        detections.append(
            {
                "box": clipped_box,
                "confidence": confidence,
                "class_id": class_id,
                "class_name": class_name,
            }
        )

    return detections


def draw_two_wheeler_boxes(
    frame_rgb: Any,
    detections: list[dict[str, object]],
) -> Any:
    annotated_frame = frame_rgb.copy()

    for detection in detections:
        x1, y1, x2, y2 = detection["box"]
        confidence = float(detection["confidence"])
        class_name = str(detection["class_name"])
        label = f"{class_name.title()} {confidence:.2f}"

        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 180, 0), 2)
        label_origin = (x1, max(y1 - 8, 18))
        cv2.putText(
            annotated_frame,
            label,
            label_origin,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 180, 0),
            2,
            cv2.LINE_AA,
        )

    return annotated_frame
