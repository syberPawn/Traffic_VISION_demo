from __future__ import annotations

from pathlib import Path
from time import perf_counter
from typing import Any, Callable

from src.detector import detect_two_wheelers, draw_two_wheeler_boxes
from src.video_utils import iter_video_frames


ProgressCallback = Callable[[int], None]


def _format_realtime_status(system_fps: float | None, input_fps: float | None) -> str:
    if system_fps is None or input_fps is None or input_fps <= 0:
        return "Unavailable: source FPS or processing FPS could not be measured."

    if system_fps >= input_fps:
        return (
            "Real-time capable for this tested video, hardware, resolution, "
            "and model configuration."
        )

    return (
        "Not fully real-time on this tested hardware for this uploaded video, "
        "resolution, and model configuration."
    )


def run_two_wheeler_fps_benchmark(
    video_path: Path,
    model: Any,
    confidence_threshold: float,
    input_fps: float | None,
    total_input_frames: int,
    progress_callback: ProgressCallback | None = None,
) -> dict[str, object]:
    started_at = perf_counter()
    processed_frames = 0
    total_detections = 0
    last_annotated_frame = None

    for frame_rgb in iter_video_frames(video_path):
        detections = detect_two_wheelers(frame_rgb, model, confidence_threshold)
        processed_frames += 1
        total_detections += len(detections)
        last_annotated_frame = draw_two_wheeler_boxes(frame_rgb, detections)

        if progress_callback is not None:
            progress_callback(processed_frames)

    processing_time_seconds = perf_counter() - started_at
    system_fps = None
    average_latency_seconds = None

    if processed_frames > 0 and processing_time_seconds > 0:
        system_fps = processed_frames / processing_time_seconds
        average_latency_seconds = processing_time_seconds / processed_frames

    input_duration_seconds = None
    if input_fps is not None and input_fps > 0 and total_input_frames > 0:
        input_duration_seconds = total_input_frames / input_fps

    real_time_factor = None
    if input_duration_seconds is not None and processing_time_seconds > 0:
        real_time_factor = input_duration_seconds / processing_time_seconds

    return {
        "input_fps": input_fps,
        "input_duration_seconds": input_duration_seconds,
        "total_input_frames": total_input_frames,
        "total_processed_frames": processed_frames,
        "total_processing_time_seconds": processing_time_seconds,
        "system_fps": system_fps,
        "average_latency_seconds": average_latency_seconds,
        "real_time_factor": real_time_factor,
        "real_time_status": _format_realtime_status(system_fps, input_fps),
        "total_detections": total_detections,
        "last_annotated_frame": last_annotated_frame,
    }
