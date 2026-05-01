from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from src.video_utils import get_video_metadata, read_first_frame, save_uploaded_video


APP_TITLE = "AI-Based Two-Wheeler Traffic Violation Detection Demo"
REGISTRY_PATH = Path("data/mock_owner_registry.json")
SUPPORTED_VIDEO_TYPES = ["mp4", "avi", "mov", "mkv"]


def ensure_registry_file() -> None:
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not REGISTRY_PATH.exists():
        REGISTRY_PATH.write_text(json.dumps({"owners": []}, indent=2), encoding="utf-8")


def load_owners() -> list[dict[str, str]]:
    ensure_registry_file()
    try:
        data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        data = {"owners": []}

    owners = data.get("owners", [])
    return owners if isinstance(owners, list) else []


def save_owner(name: str, phone: str, email: str) -> None:
    owners = load_owners()
    owners.append(
        {
            "name": name.strip(),
            "phone": phone.strip(),
            "email": email.strip(),
        }
    )
    REGISTRY_PATH.write_text(json.dumps({"owners": owners}, indent=2), encoding="utf-8")


def render_header() -> None:
    st.title(APP_TITLE)
    st.write(
        "Local academic prototype for uploaded-video based two-wheeler violation "
        "detection. This phase reads uploaded video metadata and shows a preview "
        "without running any AI model."
    )
    st.info(
        "Academic demo only: no detection, challan generation, email, or SMS is "
        "implemented in Phase 2."
    )


def render_sidebar() -> object | None:
    st.sidebar.header("Settings")
    uploaded_video = st.sidebar.file_uploader(
        "Upload traffic video",
        type=SUPPORTED_VIDEO_TYPES,
        accept_multiple_files=False,
    )
    st.sidebar.caption("Supported formats: MP4, AVI, MOV, MKV")
    return uploaded_video


def render_video_upload_status(uploaded_video: object | None) -> None:
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
    col1.metric("Input FPS", f"{fps_value:.2f}" if isinstance(fps_value, float) else "Unavailable")
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
    else:
        st.image(first_frame, caption="First readable frame", use_container_width=True)

    st.write("Frame-by-frame detection will be added in Phase 3.")


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

    uploaded_video = render_sidebar()
    render_header()
    render_video_upload_status(uploaded_video)
    render_owner_registry()


if __name__ == "__main__":
    main()
