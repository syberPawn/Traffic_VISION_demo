from __future__ import annotations

import streamlit as st

from src.benchmark import run_two_wheeler_fps_benchmark
from src.config import (
    APP_TITLE,
    SUPPORTED_VIDEO_TYPES,
    TWO_WHEELER_CONFIDENCE,
)
from src.detector import (
    detect_two_wheelers,
    draw_two_wheeler_boxes,
    load_two_wheeler_model,
)
from src.mock_database import ensure_registry_file, load_owners, save_owner
from src.video_utils import get_video_metadata, read_first_frame, save_uploaded_video


@st.cache_resource(show_spinner=False)
def get_cached_two_wheeler_model() -> object:
    return load_two_wheeler_model()


def render_header() -> None:
    st.title(APP_TITLE)
    st.write(
        "Local academic prototype for uploaded-video based two-wheeler violation "
        "detection. This phase runs two-wheeler detection and measures processing "
        "FPS on uploaded video."
    )
    st.info(
        "Academic demo only: Phase 4 measures two-wheeler detection speed only. "
        "Violation decisions and notification workflows are left for later phases."
    )


def render_sidebar() -> tuple[object | None, float]:
    st.sidebar.header("Settings")
    uploaded_video = st.sidebar.file_uploader(
        "Upload traffic video",
        type=SUPPORTED_VIDEO_TYPES,
        accept_multiple_files=False,
    )
    confidence_threshold = st.sidebar.slider(
        "Two-wheeler confidence",
        min_value=0.05,
        max_value=0.95,
        value=float(TWO_WHEELER_CONFIDENCE),
        step=0.05,
    )
    st.sidebar.caption("Supported formats: MP4, AVI, MOV, MKV")
    return uploaded_video, confidence_threshold


def render_video_upload_status(
    uploaded_video: object | None,
    confidence_threshold: float,
) -> None:
    st.subheader("Video Upload")
    if uploaded_video is None:
        st.write("Upload a traffic video from the sidebar to begin.")
        return

    st.success(f"Uploaded video: {uploaded_video.name}")
    st.video(uploaded_video)

    video_path = save_uploaded_video(uploaded_video)
    metadata = get_video_metadata(video_path)

    if not metadata["is_opened"]:
        st.error(metadata["error"] or "Unable to read uploaded video.")
        return

    fps_value = metadata["fps"]
    duration_value = metadata["duration_seconds"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "Input FPS",
        f"{fps_value:.2f}" if isinstance(fps_value, float) else "Unavailable",
    )
    col2.metric("Total Frames", f"{metadata['total_frames']}")
    col3.metric(
        "Duration",
        f"{duration_value:.2f} sec" if isinstance(duration_value, float) else "Unavailable",
    )
    col4.metric("Resolution", str(metadata["resolution"]))

    with st.expander("Video metadata", expanded=False):
        st.json(metadata)

    first_frame = read_first_frame(video_path)
    if first_frame is None:
        st.warning("OpenCV could not read a preview frame from this video.")
        return

    st.image(first_frame, caption="Original first readable frame", use_container_width=True)

    st.subheader("Two-Wheeler Detection")
    st.info("Detection is ready. Click Start Detection to annotate the first frame.")

    if st.button("Start Detection", type="primary"):
        try:
            model = get_cached_two_wheeler_model()
            detections = detect_two_wheelers(first_frame, model, confidence_threshold)
        except FileNotFoundError as exc:
            st.error(str(exc))
        except ImportError:
            st.error(
                "Ultralytics is not installed. Install dependencies with "
                "`py -m pip install -r requirements.txt`."
            )
        except Exception as exc:
            st.error(f"Two-wheeler detection failed: {exc}")
        else:
            annotated_frame = draw_two_wheeler_boxes(first_frame, detections)
            st.metric("Two-wheelers detected", len(detections))

            if detections:
                st.image(
                    annotated_frame,
                    caption="Annotated first frame",
                    use_container_width=True,
                )
                with st.expander("Detection details", expanded=False):
                    st.json(detections)
            else:
                st.warning("No two-wheelers detected on the first readable frame.")
                st.image(
                    annotated_frame,
                    caption="Annotated first frame",
                    use_container_width=True,
                )

    render_fps_benchmark(
        video_path=video_path,
        metadata=metadata,
        confidence_threshold=confidence_threshold,
    )


def render_fps_benchmark(
    video_path,
    metadata: dict[str, object],
    confidence_threshold: float,
) -> None:
    st.subheader("FPS Benchmark")
    st.caption(
        "Runs two-wheeler inference on every frame of the uploaded video and "
        "reports performance only for this tested video, hardware, resolution, "
        "and model configuration."
    )

    if not st.button("Run FPS Benchmark"):
        return

    total_input_frames = int(metadata["total_frames"] or 0)
    input_fps = metadata["fps"] if isinstance(metadata["fps"], float) else None
    progress_bar = st.progress(0.0)
    status_text = st.empty()

    def update_progress(processed_frames: int) -> None:
        if total_input_frames > 0:
            progress_bar.progress(min(processed_frames / total_input_frames, 1.0))
        status_text.write(f"Processed {processed_frames} frame(s).")

    try:
        model = get_cached_two_wheeler_model()
        benchmark = run_two_wheeler_fps_benchmark(
            video_path=video_path,
            model=model,
            confidence_threshold=confidence_threshold,
            input_fps=input_fps,
            total_input_frames=total_input_frames,
            progress_callback=update_progress,
        )
    except FileNotFoundError as exc:
        st.error(str(exc))
        return
    except ImportError:
        st.error(
            "Ultralytics is not installed. Install dependencies with "
            "`py -m pip install -r requirements.txt`."
        )
        return
    except Exception as exc:
        st.error(f"FPS benchmark failed: {exc}")
        return

    progress_bar.progress(1.0)
    status_text.write("Benchmark complete.")
    render_benchmark_results(benchmark)


def render_benchmark_results(benchmark: dict[str, object]) -> None:
    input_fps = benchmark["input_fps"]
    input_duration = benchmark["input_duration_seconds"]
    processing_time = benchmark["total_processing_time_seconds"]
    system_fps = benchmark["system_fps"]
    average_latency = benchmark["average_latency_seconds"]
    real_time_factor = benchmark["real_time_factor"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "Input Video FPS",
        f"{input_fps:.2f}" if isinstance(input_fps, float) else "Unavailable",
    )
    col2.metric(
        "Input Duration",
        f"{input_duration:.2f} sec" if isinstance(input_duration, float) else "Unavailable",
    )
    col3.metric("Frames Processed", str(benchmark["total_processed_frames"]))
    col4.metric(
        "Processing Time",
        f"{processing_time:.2f} sec" if isinstance(processing_time, float) else "Unavailable",
    )

    col5, col6, col7, col8 = st.columns(4)
    col5.metric(
        "System FPS",
        f"{system_fps:.2f}" if isinstance(system_fps, float) else "Unavailable",
    )
    col6.metric(
        "Avg Latency",
        f"{average_latency * 1000:.2f} ms" if isinstance(average_latency, float) else "Unavailable",
    )
    col7.metric(
        "Real-Time Factor",
        f"{real_time_factor:.2f}x" if isinstance(real_time_factor, float) else "Unavailable",
    )
    col8.metric("Detections", str(benchmark["total_detections"]))

    st.info(str(benchmark["real_time_status"]))

    if benchmark["last_annotated_frame"] is not None:
        st.image(
            benchmark["last_annotated_frame"],
            caption="Last processed frame",
            use_container_width=True,
        )


def render_owner_registry() -> None:
    st.subheader("Mock Owner Registry")
    st.caption(
        "Demo owner details are stored locally in data/mock_owner_registry.json."
    )

    with st.form("owner_registry_form", clear_on_submit=True):
        owner_name = st.text_input("Owner name")
        phone_number = st.text_input("Phone number")
        email_address = st.text_input("Email address")
        submitted = st.form_submit_button("Save owner")

    if submitted:
        if owner_name.strip() and phone_number.strip() and email_address.strip():
            save_owner(owner_name, phone_number, email_address)
            st.success("Owner saved.")
        else:
            st.warning("Enter owner name, phone number, and email address.")

    owners = load_owners()
    st.markdown("#### Saved Owners")
    if owners:
        st.dataframe(owners, use_container_width=True, hide_index=True)
    else:
        st.write("No demo owners saved yet.")


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    ensure_registry_file()

    uploaded_video, confidence_threshold = render_sidebar()
    render_header()
    render_video_upload_status(uploaded_video, confidence_threshold)
    render_owner_registry()


if __name__ == "__main__":
    main()
