from __future__ import annotations

import asyncio
from datetime import datetime
import importlib
import inspect
import json
import os
import pathlib
import random
from pathlib import Path
import sys
from time import perf_counter

if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import cv2
import imageio.v2 as imageio
import streamlit as st


APP_TITLE = "Simple Two-Wheeler Violation Demo"
APP_STATE_VERSION = "ocr-plate-text-v2"

MODELS_DIR = Path("models")
OUTPUTS_DIR = Path("outputs")
PROCESSED_DIR = OUTPUTS_DIR / "processed_videos"
UPLOAD_DIR = OUTPUTS_DIR / "uploads"
EVIDENCE_DIR = OUTPUTS_DIR / "evidence"
CHALLAN_DIR = OUTPUTS_DIR / "challans"
OWNER_DB_PATH = OUTPUTS_DIR / "mock_owners.json"
SMS_LOG_PATH = OUTPUTS_DIR / "demo_sms_log.csv"
YOLO_CONFIG_DIR = Path("tmp") / "ultralytics"
YOLO_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("YOLO_CONFIG_DIR", str(YOLO_CONFIG_DIR))
os.environ.setdefault("YOLOV5_CONFIG_DIR", str(YOLO_CONFIG_DIR))
os.environ.setdefault("YOLOv5_AUTOINSTALL", "false")

TWO_WHEELER_MODEL_PATH = MODELS_DIR / "two-wheeler.pt"
NANO_TWO_WHEELER_MODEL_PATH = MODELS_DIR / "two-wheeler-nano.pt"
NANO_TWO_WHEELER_MODEL_SOURCE = "yolov8n.pt"
HELMET_MODEL_PATH = MODELS_DIR / "helmet-detection.pt"
POSE_MODEL_PATH = MODELS_DIR / "yolov8n-pose.pt"
ALPR_MODEL_PATH = MODELS_DIR / "alpr.pt"
EASYOCR_MODEL_DIR = MODELS_DIR / "easyocr"

MODEL_IMAGE_SIZE = 640
MAX_PROCESS_WIDTH = 1280
BIKE_CONFIDENCE = 0.35
HELMET_CONFIDENCE = 0.35
POSE_CONFIDENCE = 0.25
ALPR_CONFIDENCE = 0.25
MAX_DISPLAY_VIOLATIONS = 200
COCO_TWO_WHEELER_CLASSES = {"motorcycle", "bicycle"}
TRACK_IOU_THRESHOLD = 0.30
VIOLATION_SEVERITY = {
    "No Violation": 0,
    "No Helmet": 1,
    "Triple Riding": 1,
    "No Helmet + Triple Riding": 2,
}
FINE_AMOUNTS = {
    "No Helmet": 500,
    "Triple Riding": 1000,
    "No Helmet + Triple Riding": 1500,
}


def cuda_is_available() -> bool:
    try:
        import torch

        return bool(torch.cuda.is_available())
    except Exception:
        return False


def cuda_device_name() -> str:
    try:
        import torch

        if torch.cuda.is_available():
            return str(torch.cuda.get_device_name(0))
    except Exception:
        pass
    return "CPU"


def resolve_device(device_choice: str) -> str | int:
    if device_choice == "GPU" and cuda_is_available():
        return 0
    if device_choice == "Auto" and cuda_is_available():
        return 0
    return "cpu"


@st.cache_resource(show_spinner=False)
def load_model(source: str | Path):
    if isinstance(source, Path) and not source.exists():
        raise FileNotFoundError(f"Model not found: {source}")

    prepare_yolo_runtime(source)
    from ultralytics import YOLO

    return patch_legacy_model(YOLO(str(source)))


@st.cache_resource(show_spinner=False)
def load_ocr_reader():
    import easyocr

    EASYOCR_MODEL_DIR.mkdir(parents=True, exist_ok=True)
    return easyocr.Reader(
        ["en"],
        gpu=False,
        model_storage_directory=str(EASYOCR_MODEL_DIR),
        user_network_directory=str(EASYOCR_MODEL_DIR),
    )


def prepare_yolo_runtime(source: str | Path) -> None:
    if os.name == "nt":
        pathlib.PosixPath = pathlib.WindowsPath

    source_name = source.name if isinstance(source, Path) else str(source)
    if source_name in {HELMET_MODEL_PATH.name, ALPR_MODEL_PATH.name}:
        for alias, target in {
            "models": "yolov5.models",
            "models.yolo": "yolov5.models.yolo",
            "models.common": "yolov5.models.common",
            "models.experimental": "yolov5.models.experimental",
        }.items():
            try:
                sys.modules.setdefault(alias, importlib.import_module(target))
            except ImportError:
                pass


def patch_legacy_model(model):
    loaded_model = getattr(model, "model", None)
    if loaded_model is None:
        return model

    if hasattr(loaded_model, "fuse"):
        fuse_method = loaded_model.fuse
        if "verbose" not in inspect.signature(fuse_method).parameters:
            def fuse_compatible(verbose: bool = True):
                return fuse_method()

            loaded_model.fuse = fuse_compatible

    if hasattr(loaded_model, "forward"):
        forward_method = loaded_model.forward
        if "embed" not in inspect.signature(forward_method).parameters:
            def forward_compatible(*args, **kwargs):
                kwargs.pop("embed", None)
                return forward_method(*args, **kwargs)

            loaded_model.forward = forward_compatible

    return model


def save_upload(uploaded_file) -> Path:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    output_path = UPLOAD_DIR / uploaded_file.name
    output_path.write_bytes(uploaded_file.getbuffer())
    return output_path


def load_owners() -> list[dict[str, str]]:
    if not OWNER_DB_PATH.exists():
        return []

    try:
        owners = json.loads(OWNER_DB_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(owners, list):
        return []

    cleaned = []
    for owner in owners:
        if not isinstance(owner, dict):
            continue
        cleaned.append(
            {
                "name": str(owner.get("name", "")).strip(),
                "phone": str(owner.get("phone", "")).strip(),
                "email": str(owner.get("email", "")).strip(),
            }
        )
    return cleaned


def save_owner(name: str, phone: str, email: str) -> None:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    owners = load_owners()
    owners.append(
        {
            "name": name.strip(),
            "phone": phone.strip(),
            "email": email.strip(),
        }
    )
    OWNER_DB_PATH.write_text(json.dumps(owners, indent=2), encoding="utf-8")


def choose_demo_owner(owners: list[dict[str, str]]) -> dict[str, str] | None:
    if not owners:
        return None
    return random.choice(owners)


def log_demo_sms(track_id: int, phone: str, violation: str) -> str:
    if not phone:
        return "No phone number available"

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    is_new_file = not SMS_LOG_PATH.exists()
    with SMS_LOG_PATH.open("a", encoding="utf-8") as log_file:
        if is_new_file:
            log_file.write("timestamp,track_id,phone,violation,status\n")
        log_file.write(f"{datetime.now().isoformat(timespec='seconds')},T{track_id},{phone},{violation},sent\n")
    return f"SMS sent to {phone}"


def resize_for_processing(frame_rgb):
    height, width = frame_rgb.shape[:2]
    if width <= MAX_PROCESS_WIDTH:
        return frame_rgb

    scale = MAX_PROCESS_WIDTH / width
    resized_width = MAX_PROCESS_WIDTH
    resized_height = int(round(height * scale))
    resized_height = max(16, (resized_height // 16) * 16)
    return cv2.resize(frame_rgb, (resized_width, resized_height), interpolation=cv2.INTER_AREA)


def render_dataframe(rows: list[dict[str, object]]) -> None:
    display_rows = [
        {key: "" if value is None else str(value) for key, value in row.items()}
        for row in rows
    ]
    try:
        st.dataframe(display_rows, width="stretch", hide_index=True)
    except TypeError:
        st.dataframe(display_rows, use_container_width=True, hide_index=True)


def render_video_file(path: Path) -> None:
    try:
        st.video(str(path), format="video/mp4")
    except Exception:
        st.video(path.read_bytes(), format="video/mp4")


def render_processing_result(result: dict[str, object]) -> None:
    st.subheader("Processed Video")
    render_video_file(Path(str(result["output_path"])))

    render_processing_info_card(result)

    st.subheader("Violation Information")
    if result["violations"]:
        render_dataframe(result["violations"])
        render_challan_downloads(result["violations"])
    else:
        st.success("No violations detected.")


def render_challan_downloads(rows: list[dict[str, object]]) -> None:
    st.subheader("Generated Challans")
    for row in rows:
        pdf_path = Path(str(row.get("challan_pdf_path", "")))
        if not pdf_path.exists():
            continue
        track_id = row.get("track_id", "")
        with pdf_path.open("rb") as pdf_file:
            st.download_button(
                label=f"Download challan for T{track_id}",
                data=pdf_file,
                file_name=pdf_path.name,
                mime="application/pdf",
            )


def render_owner_database() -> None:
    st.subheader("Mock Owner Database")
    st.caption("Owner lookup is randomly assigned for academic demo purposes.")

    with st.form("owner_form", clear_on_submit=True):
        owner_name = st.text_input("Owner name")
        phone_number = st.text_input("Phone number")
        email_address = st.text_input("Email address")
        submitted = st.form_submit_button("Save owner")

    if submitted:
        if owner_name.strip() and phone_number.strip():
            save_owner(owner_name, phone_number, email_address)
            st.success("Owner saved.")
        else:
            st.warning("Owner name and phone number are required.")

    owners = load_owners()
    if owners:
        render_dataframe(owners)
    else:
        st.info("No owners saved yet. Violations will show no owner phone available.")


def clip_box(box: list[float], width: int, height: int) -> list[int] | None:
    x1, y1, x2, y2 = [int(round(value)) for value in box]
    x1 = max(0, min(x1, width - 1))
    y1 = max(0, min(y1, height - 1))
    x2 = max(0, min(x2, width - 1))
    y2 = max(0, min(y2, height - 1))
    if x2 <= x1 or y2 <= y1:
        return None
    return [x1, y1, x2, y2]


def expand_bike_box(box: list[int], width: int, height: int) -> list[int]:
    x1, y1, x2, y2 = box
    box_width = x2 - x1
    box_height = y2 - y1
    return [
        max(0, int(x1 - box_width * 0.15)),
        max(0, int(y1 - box_height * 1.20)),
        min(width - 1, int(x2 + box_width * 0.15)),
        min(height - 1, y2),
    ]


def yolo_detections(
    model,
    image,
    confidence: float,
    device: str | int,
    allowed_class_names: set[str] | None = None,
) -> list[dict[str, object]]:
    height, width = image.shape[:2]
    try:
        results = model.predict(
            image,
            conf=confidence,
            imgsz=MODEL_IMAGE_SIZE,
            device=device,
            half=device != "cpu",
            verbose=False,
        )
    except RuntimeError as exc:
        if device == "cpu" or "cuda" not in str(exc).lower():
            raise
        try:
            import torch

            torch.cuda.empty_cache()
        except Exception:
            pass
        results = model.predict(
            image,
            conf=confidence,
            imgsz=MODEL_IMAGE_SIZE,
            device="cpu",
            verbose=False,
        )
    finally:
        if device != "cpu":
            try:
                import torch

                torch.cuda.empty_cache()
            except Exception:
                pass

    if not results or results[0].boxes is None:
        return []

    names = results[0].names or getattr(model, "names", {}) or {}
    detections: list[dict[str, object]] = []
    for item in results[0].boxes:
        box = clip_box(item.xyxy[0].tolist(), width, height)
        if box is None:
            continue
        class_id = int(item.cls[0])
        class_name = str(names.get(class_id, class_id))
        if allowed_class_names is not None and class_name.lower() not in allowed_class_names:
            continue
        detections.append(
            {
                "box": box,
                "confidence": float(item.conf[0]),
                "class_name": class_name,
            }
        )
    return detections


def two_wheeler_model_source(detector_choice: str) -> str | Path:
    if detector_choice.startswith("Smaller"):
        if NANO_TWO_WHEELER_MODEL_PATH.exists():
            return NANO_TWO_WHEELER_MODEL_PATH
        return NANO_TWO_WHEELER_MODEL_SOURCE
    return TWO_WHEELER_MODEL_PATH


def two_wheeler_allowed_classes(detector_choice: str) -> set[str] | None:
    if detector_choice.startswith("Smaller"):
        return COCO_TWO_WHEELER_CLASSES
    return None


def helmet_status(helmet_detections: list[dict[str, object]]) -> str:
    names = [str(item["class_name"]).lower().replace(" ", "_") for item in helmet_detections]
    has_helmet = any("with_helmet" in name or name == "helmet" for name in names)
    has_no_helmet = any("without_helmet" in name or "no_helmet" in name for name in names)

    if has_helmet:
        return "Helmet Present"
    if has_no_helmet:
        return "No Helmet"
    return "Unknown"


def detect_helmet_in_bike_crop(
    frame,
    region: list[int],
    helmet_model,
    device: str | int,
) -> tuple[str, list[dict[str, object]]]:
    x1, y1, x2, y2 = region
    crop = frame[y1:y2, x1:x2]
    if crop.size == 0:
        return "Unknown", []

    detections = yolo_detections(helmet_model, crop, HELMET_CONFIDENCE, device)
    shifted = []
    for detection in detections:
        hx1, hy1, hx2, hy2 = detection["box"]
        shifted_detection = dict(detection)
        shifted_detection["box"] = [hx1 + x1, hy1 + y1, hx2 + x1, hy2 + y1]
        shifted.append(shifted_detection)

    return helmet_status(shifted), shifted


def count_riders(people: list[dict[str, object]], region: list[int]) -> tuple[int, list[dict[str, object]]]:
    x1, y1, x2, y2 = region
    riders = []
    for person in people:
        px1, py1, px2, py2 = person["box"]
        center_x = int((px1 + px2) / 2)
        center_y = int((py1 + py2) / 2)
        if x1 <= center_x <= x2 and y1 <= center_y <= y2:
            riders.append(person)
    return len(riders), riders


def violation_type(status: str, rider_count: int) -> str:
    no_helmet = status == "No Helmet"
    triple_riding = rider_count >= 3
    if no_helmet and triple_riding:
        return "No Helmet + Triple Riding"
    if no_helmet:
        return "No Helmet"
    if triple_riding:
        return "Triple Riding"
    return "No Violation"


def clean_plate_text(text: str) -> str:
    cleaned = "".join(character for character in text.upper() if character.isalnum())
    return cleaned or "Unreadable"


def read_plate_text(plate_crop, ocr_reader) -> tuple[str, float]:
    if plate_crop.size == 0:
        return "Unreadable", 0.0

    enlarged = cv2.resize(plate_crop, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    try:
        results = ocr_reader.readtext(enlarged)
    except Exception:
        return "Unreadable", 0.0

    best_text = "Unreadable"
    best_confidence = 0.0
    for result in results:
        if len(result) < 3:
            continue
        text = clean_plate_text(str(result[1]))
        confidence = float(result[2])
        if text != "Unreadable" and confidence > best_confidence:
            best_text = text
            best_confidence = confidence

    return best_text, best_confidence


def find_plate(
    frame,
    region: list[int],
    alpr_model,
    ocr_reader,
    device: str | int,
) -> tuple[str, list[dict[str, object]]]:
    x1, y1, x2, y2 = region
    crop = frame[y1:y2, x1:x2]
    if crop.size == 0:
        return "Not detected", []

    detections = yolo_detections(alpr_model, crop, ALPR_CONFIDENCE, device)
    shifted = []
    for detection in detections:
        px1, py1, px2, py2 = detection["box"]
        shifted_detection = dict(detection)
        shifted_detection["box"] = [px1 + x1, py1 + y1, px2 + x1, py2 + y1]
        shifted.append(shifted_detection)

    if not shifted:
        return "Not detected", []
    best = max(shifted, key=lambda item: float(item["confidence"]))
    px1, py1, px2, py2 = best["box"]
    plate_crop = frame[py1:py2, px1:px2]
    plate_text, ocr_confidence = read_plate_text(plate_crop, ocr_reader)
    if plate_text == "Unreadable":
        return f"OCR unreadable (ALPR box confidence {float(best['confidence']):.2f})", shifted
    return f"{plate_text} (ocr {ocr_confidence:.2f}, box {float(best['confidence']):.2f})", shifted


def draw_box(frame, box: list[int], color: tuple[int, int, int], label: str) -> None:
    x1, y1, x2, y2 = box
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    cv2.putText(
        frame,
        label,
        (x1, max(20, y1 - 8)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        color,
        2,
        cv2.LINE_AA,
    )


def frame_timestamp(frame_index: int, fps: float) -> str:
    if fps <= 0:
        return "00:00.000"

    total_seconds = frame_index / fps
    minutes = int(total_seconds // 60)
    seconds = total_seconds - minutes * 60
    return f"{minutes:02d}:{seconds:06.3f}"


def save_evidence_snapshot(
    frame_rgb,
    region: list[int],
    track_id: int,
    frame_index: int,
    violation: str,
    timestamp: str,
) -> str:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    x1, y1, x2, y2 = region
    crop = frame_rgb[y1:y2, x1:x2].copy()
    if crop.size == 0:
        crop = frame_rgb.copy()

    cv2.rectangle(crop, (0, 0), (crop.shape[1] - 1, crop.shape[0] - 1), (220, 0, 0), 4)
    cv2.putText(
        crop,
        f"T{track_id} {violation}",
        (10, 28),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (220, 0, 0),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        crop,
        f"Time {timestamp} | Frame {frame_index}",
        (10, min(crop.shape[0] - 12, 58)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (220, 0, 0),
        2,
        cv2.LINE_AA,
    )

    evidence_path = EVIDENCE_DIR / f"evidence_T{track_id}_F{frame_index}.jpg"
    saved = cv2.imwrite(str(evidence_path), cv2.cvtColor(crop, cv2.COLOR_RGB2BGR))
    if not saved:
        raise RuntimeError(f"Could not save evidence image: {evidence_path}")
    return str(evidence_path)


def generate_challan_pdf(track: dict[str, object], fps: float) -> str:
    CHALLAN_DIR.mkdir(parents=True, exist_ok=True)
    track_id = int(track["track_id"])
    violation = str(track.get("violation", ""))
    fine_amount = FINE_AMOUNTS.get(violation, 0)
    violation_frame = int(track.get("violation_frame", 0) or 0)
    timestamp = frame_timestamp(violation_frame, fps)
    evidence_path = str(track.get("evidence_image_path", ""))
    pdf_path = CHALLAN_DIR / f"challan_T{track_id}_F{violation_frame}.pdf"

    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    styles = getSampleStyleSheet()
    document = SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36)
    story = [
        Paragraph("Traffic Violation Challan", styles["Title"]),
        Paragraph("Academic demo document. Not a legal traffic challan.", styles["Normal"]),
        Spacer(1, 0.2 * inch),
    ]

    details = [
        ["Track ID", f"T{track_id}"],
        ["Timestamp", timestamp],
        ["Frame", str(violation_frame)],
        ["Violation Type", violation],
        ["Fine Amount", f"Rs. {fine_amount}"],
        ["Helmet Status", str(track.get("helmet_status", ""))],
        ["Rider Count", str(track.get("rider_count", ""))],
        ["Plate Result", str(track.get("best_plate", "Not detected"))],
        ["Owner Name", str(track.get("owner_name", ""))],
        ["Owner Phone", str(track.get("owner_phone", ""))],
        ["Owner Email", str(track.get("owner_email", ""))],
        ["Demo SMS Status", str(track.get("sms_status", ""))],
    ]
    table = Table(details, colWidths=[1.8 * inch, 4.6 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f0f3f6")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#c9d1d9")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.extend([table, Spacer(1, 0.25 * inch)])

    if evidence_path and Path(evidence_path).exists():
        story.append(Paragraph("Violation Evidence", styles["Heading2"]))
        story.append(Image(evidence_path, width=5.8 * inch, height=3.4 * inch, kind="proportional"))

    document.build(story)
    return str(pdf_path)


def box_iou(first_box: list[int], second_box: list[int]) -> float:
    ax1, ay1, ax2, ay2 = first_box
    bx1, by1, bx2, by2 = second_box

    intersection_x1 = max(ax1, bx1)
    intersection_y1 = max(ay1, by1)
    intersection_x2 = min(ax2, bx2)
    intersection_y2 = min(ay2, by2)
    intersection_width = max(0, intersection_x2 - intersection_x1)
    intersection_height = max(0, intersection_y2 - intersection_y1)
    intersection_area = intersection_width * intersection_height

    first_area = max(0, ax2 - ax1) * max(0, ay2 - ay1)
    second_area = max(0, bx2 - bx1) * max(0, by2 - by1)
    union_area = first_area + second_area - intersection_area
    if union_area <= 0:
        return 0.0

    return intersection_area / union_area


def assign_track_id(
    bike_box: list[int],
    tracks: dict[int, dict[str, object]],
    used_track_ids: set[int],
    next_track_id: int,
    frame_index: int,
) -> tuple[int, int]:
    best_track_id = None
    best_iou = 0.0

    for track_id, track in tracks.items():
        if track_id in used_track_ids:
            continue
        previous_box = track.get("box")
        if not isinstance(previous_box, list):
            continue
        current_iou = box_iou(bike_box, previous_box)
        if current_iou > best_iou:
            best_iou = current_iou
            best_track_id = track_id

    if best_track_id is None or best_iou < TRACK_IOU_THRESHOLD:
        best_track_id = next_track_id
        next_track_id += 1
        tracks[best_track_id] = {
            "track_id": best_track_id,
            "first_frame": frame_index,
            "violation_detected": False,
            "best_plate": "Not detected",
            "best_plate_score": 0.0,
        }

    tracks[best_track_id]["box"] = bike_box
    tracks[best_track_id]["last_seen_frame"] = frame_index
    used_track_ids.add(best_track_id)
    return best_track_id, next_track_id


def plate_score(plate_boxes: list[dict[str, object]]) -> float:
    if not plate_boxes:
        return 0.0

    best_score = 0.0
    for plate in plate_boxes:
        box = plate.get("box")
        if not isinstance(box, list) or len(box) < 4:
            continue
        x1, y1, x2, y2 = box
        area = max(0, x2 - x1) * max(0, y2 - y1)
        confidence = float(plate.get("confidence", 0.0))
        best_score = max(best_score, confidence * area)
    return best_score


def update_violation_track(
    track: dict[str, object],
    frame_index: int,
    violation: str,
    helmet_status_value: str,
    rider_count: int,
    plate_text: str,
    plate_boxes: list[dict[str, object]],
    evidence_image_path: str,
) -> None:
    track["violation_detected"] = True
    track.setdefault("violation_frame", frame_index)
    track.setdefault("evidence_image_path", evidence_image_path)

    existing_violation = str(track.get("violation", "No Violation"))
    if VIOLATION_SEVERITY.get(violation, 0) >= VIOLATION_SEVERITY.get(existing_violation, 0):
        track["violation"] = violation
        track["helmet_status"] = helmet_status_value
        track["rider_count"] = rider_count
        track["fine_amount"] = FINE_AMOUNTS.get(violation, 0)

    current_plate_score = plate_score(plate_boxes)
    if current_plate_score > float(track.get("best_plate_score", 0.0)):
        track["best_plate"] = plate_text
        track["best_plate_score"] = current_plate_score
        track["best_plate_frame"] = frame_index


def assign_mock_owner_and_sms(track: dict[str, object], owners: list[dict[str, str]]) -> None:
    if track.get("owner_assigned"):
        return

    owner = choose_demo_owner(owners)
    if owner is None:
        track["owner_name"] = "No owner saved"
        track["owner_phone"] = ""
        track["owner_email"] = ""
        track["sms_status"] = "No owner phone available"
        track["owner_assigned"] = True
        return

    track["owner_name"] = owner.get("name", "")
    track["owner_phone"] = owner.get("phone", "")
    track["owner_email"] = owner.get("email", "")
    track["sms_status"] = log_demo_sms(
        track_id=int(track["track_id"]),
        phone=str(owner.get("phone", "")),
        violation=str(track.get("violation", "")),
    )
    track["owner_assigned"] = True


def generate_challans_for_tracks(
    tracks: dict[int, dict[str, object]],
    fps: float,
    owners: list[dict[str, str]],
) -> None:
    for track in tracks.values():
        if not track.get("violation_detected"):
            continue
        assign_mock_owner_and_sms(track, owners)
        if track.get("challan_pdf_path"):
            continue
        track["challan_pdf_path"] = generate_challan_pdf(track, fps)


def build_violation_rows(tracks: dict[int, dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for track_id in sorted(tracks):
        track = tracks[track_id]
        if not track.get("violation_detected"):
            continue
        rows.append(
            {
                "track_id": track_id,
                "first_frame": track.get("first_frame", ""),
                "last_seen_frame": track.get("last_seen_frame", ""),
                "violation_frame": track.get("violation_frame", ""),
                "violation": track.get("violation", ""),
                "fine_amount": track.get("fine_amount", ""),
                "helmet_status": track.get("helmet_status", ""),
                "rider_count": track.get("rider_count", ""),
                "plate": track.get("best_plate", "Not detected"),
                "plate_frame": track.get("best_plate_frame", ""),
                "owner_name": track.get("owner_name", ""),
                "owner_phone": track.get("owner_phone", ""),
                "owner_email": track.get("owner_email", ""),
                "sms_status": track.get("sms_status", ""),
                "evidence_image_path": track.get("evidence_image_path", ""),
                "challan_pdf_path": track.get("challan_pdf_path", ""),
            }
        )
        if len(rows) >= MAX_DISPLAY_VIOLATIONS:
            break
    return rows


def process_video(
    video_path: Path,
    frame_stride: int = 1,
    device_choice: str = "Auto",
    detector_choice: str = "Current custom detector",
) -> dict[str, object]:
    bike_model = load_model(two_wheeler_model_source(detector_choice))
    helmet_model = load_model(HELMET_MODEL_PATH)
    pose_model = load_model(POSE_MODEL_PATH)
    alpr_model = load_model(ALPR_MODEL_PATH)
    ocr_reader = load_ocr_reader()
    device = resolve_device(device_choice)
    bike_allowed_classes = two_wheeler_allowed_classes(detector_choice)
    owners = load_owners()

    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise RuntimeError("Could not open uploaded video.")

    fps = capture.get(cv2.CAP_PROP_FPS) or 20.0
    output_path = PROCESSED_DIR / f"processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    writer = imageio.get_writer(
        str(output_path),
        fps=float(fps),
        codec="libx264",
        macro_block_size=16,
        ffmpeg_params=["-movflags", "+faststart"],
    )

    frame_count = 0
    tracks: dict[int, dict[str, object]] = {}
    next_track_id = 1
    started_at = perf_counter()

    try:
        while True:
            ok, frame_bgr = capture.read()
            if not ok:
                break

            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            frame_rgb = resize_for_processing(frame_rgb)
            if frame_stride > 1 and frame_count % frame_stride != 0:
                writer.append_data(frame_rgb)
                frame_count += 1
                continue

            height, width = frame_rgb.shape[:2]
            bikes = yolo_detections(
                bike_model,
                frame_rgb,
                BIKE_CONFIDENCE,
                device,
                allowed_class_names=bike_allowed_classes,
            )
            people = yolo_detections(pose_model, frame_rgb, POSE_CONFIDENCE, device) if bikes else []
            used_track_ids: set[int] = set()

            for bike_index, bike in enumerate(bikes, start=1):
                bike_box = bike["box"]
                track_id, next_track_id = assign_track_id(
                    bike_box=bike_box,
                    tracks=tracks,
                    used_track_ids=used_track_ids,
                    next_track_id=next_track_id,
                    frame_index=frame_count,
                )
                region = expand_bike_box(bike_box, width, height)
                status, helmet_boxes = detect_helmet_in_bike_crop(frame_rgb, region, helmet_model, device)
                rider_count, rider_boxes = count_riders(people, region)
                violation = violation_type(status, rider_count)
                plate_text = "Skipped"
                plate_boxes = []

                if violation != "No Violation":
                    evidence_image_path = save_evidence_snapshot(
                        frame_rgb=frame_rgb,
                        region=region,
                        track_id=track_id,
                        frame_index=frame_count,
                        violation=violation,
                        timestamp=frame_timestamp(frame_count, fps),
                    )
                    plate_text, plate_boxes = find_plate(frame_rgb, region, alpr_model, ocr_reader, device)
                    update_violation_track(
                        track=tracks[track_id],
                        frame_index=frame_count,
                        violation=violation,
                        helmet_status_value=status,
                        rider_count=rider_count,
                        plate_text=plate_text,
                        plate_boxes=plate_boxes,
                        evidence_image_path=evidence_image_path,
                    )

                color = (0, 180, 0) if violation == "No Violation" else (220, 0, 0)
                draw_box(frame_rgb, region, color, f"T{track_id} {violation} | riders {rider_count}")
                draw_box(frame_rgb, bike_box, (0, 160, 255), f"Bike T{track_id}")

                for helmet_box in helmet_boxes:
                    draw_box(frame_rgb, helmet_box["box"], (255, 120, 0), str(helmet_box["class_name"]))
                for rider in rider_boxes:
                    draw_box(frame_rgb, rider["box"], (0, 120, 255), "Rider")
                for plate in plate_boxes:
                    draw_box(frame_rgb, plate["box"], (255, 255, 0), "Plate")

            writer.append_data(frame_rgb)
            frame_count += 1
    finally:
        capture.release()
        writer.close()

    elapsed = max(perf_counter() - started_at, 0.001)
    generate_challans_for_tracks(tracks, fps, owners)
    violation_rows = build_violation_rows(tracks)
    return {
        "output_path": output_path,
        "frames": frame_count,
        "seconds": elapsed,
        "fps": frame_count / elapsed,
        "device": cuda_device_name() if device != "cpu" else "CPU",
        "detector": detector_choice,
        "violations": violation_rows,
    }


def render_processing_info_card(result: dict[str, object]) -> None:
    frames = int(result["frames"])
    fps = float(result["fps"])
    seconds = float(result["seconds"])
    device = str(result.get("device", "CPU"))
    detector = str(result.get("detector", "Current custom detector"))
    charged_tracks = len(result.get("violations", []))

    st.markdown(
        f"""
        <div style="
            border: 1px solid #b6c2cf;
            border-radius: 8px;
            padding: 18px 20px;
            margin: 16px 0 20px 0;
            background: #f6f8fa;
            color: #111827;
        ">
            <div style="font-size: 18px; font-weight: 700; margin-bottom: 14px;">
                Processing Information
            </div>
            <div style="
                display: grid;
                grid-template-columns: repeat(6, minmax(0, 1fr));
                gap: 14px;
            ">
                <div style="background: #ffffff; border: 1px solid #d0d7de; border-radius: 6px; padding: 12px;">
                    <div style="font-size: 13px; color: #374151; font-weight: 600;">Operating FPS</div>
                    <div style="font-size: 26px; font-weight: 700;">{fps:.2f}</div>
                </div>
                <div style="background: #ffffff; border: 1px solid #d0d7de; border-radius: 6px; padding: 12px;">
                    <div style="font-size: 13px; color: #374151; font-weight: 600;">Total Frames</div>
                    <div style="font-size: 26px; font-weight: 700;">{frames}</div>
                </div>
                <div style="background: #ffffff; border: 1px solid #d0d7de; border-radius: 6px; padding: 12px;">
                    <div style="font-size: 13px; color: #374151; font-weight: 600;">Time Taken</div>
                    <div style="font-size: 26px; font-weight: 700;">{seconds:.2f}s</div>
                </div>
                <div style="background: #ffffff; border: 1px solid #d0d7de; border-radius: 6px; padding: 12px;">
                    <div style="font-size: 13px; color: #374151; font-weight: 600;">Device</div>
                    <div style="font-size: 18px; font-weight: 700;">{device}</div>
                </div>
                <div style="background: #ffffff; border: 1px solid #d0d7de; border-radius: 6px; padding: 12px;">
                    <div style="font-size: 13px; color: #374151; font-weight: 600;">Bike Detector</div>
                    <div style="font-size: 18px; font-weight: 700;">{detector}</div>
                </div>
                <div style="background: #ffffff; border: 1px solid #d0d7de; border-radius: 6px; padding: 12px;">
                    <div style="font-size: 13px; color: #374151; font-weight: 600;">Unique Charges</div>
                    <div style="font-size: 26px; font-weight: 700;">{charged_tracks}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    st.title(APP_TITLE)

    if st.session_state.get("app_state_version") != APP_STATE_VERSION:
        st.session_state.clear()
        st.session_state["app_state_version"] = APP_STATE_VERSION

    render_owner_database()

    uploaded_video = st.file_uploader("Upload a traffic video", type=["mp4", "avi", "mov", "mkv"])
    if uploaded_video is None:
        st.info("Upload a video and click Process Video.")
        return

    frame_stride = st.selectbox(
        "Speed mode",
        options=[1, 2, 3, 5],
        format_func=lambda value: "Best accuracy" if value == 1 else f"Faster: process every {value}th frame",
    )
    detector_choice = st.selectbox(
        "Two-wheeler detector",
        options=[
            "Current custom detector",
            "Smaller COCO nano detector",
        ],
        help=(
            "The smaller option uses models/two-wheeler-nano.pt if present; "
            "otherwise it downloads yolov8n.pt and filters detections to "
            "motorcycle/bicycle classes."
        ),
    )
    device_choice = st.selectbox(
        "Inference device",
        options=["Auto", "GPU", "CPU"],
        help="Use GPU only from the D: virtual environment where torch.cuda.is_available() is True.",
    )

    video_path = save_upload(uploaded_video)
    st.video(uploaded_video, format="video/mp4")

    if st.button("Clear processed result"):
        st.session_state.pop("last_result", None)

    if "last_result" in st.session_state:
        render_processing_result(st.session_state["last_result"])

    if st.button("Process Video", type="primary"):
        with st.spinner("Processing video..."):
            try:
                result = process_video(
                    video_path,
                    frame_stride=int(frame_stride),
                    device_choice=str(device_choice),
                    detector_choice=str(detector_choice),
                )
            except Exception as exc:
                st.error(f"Processing failed: {exc}")
                st.exception(exc)
                return

        st.session_state["last_result"] = result
        render_processing_result(result)


if __name__ == "__main__":
    main()
