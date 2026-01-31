import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import tempfile
import pandas as pd

st.set_page_config(page_title="AI Workout Analysis", layout="wide")
st.title("🏋️ AI Workout Motion & Injury Risk Analysis")

st.markdown("""
Upload your workout video.  
The system will analyze **rep quality**, **depth**, and **potential injury risk moments**.
""")
# ================== SIDEBAR SETTINGS ==================
st.sidebar.header("⚙️ Analysis Settings")

GOOD_T = st.sidebar.slider("Good Rep Threshold", 0.015, 0.03, 0.022)
BAD_T = st.sidebar.slider("Bad Rep Threshold", 0.008, 0.02, 0.013)
# ================= Upload Video =================
video_file = st.file_uploader("Upload workout video", type=["mp4", "mov", "avi"])

if video_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())
    video_path = tfile.name

    st.video(video_file)

    # ================= MediaPipe Setup =================
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    cap = cv2.VideoCapture(video_path)
    FPS = cap.get(cv2.CAP_PROP_FPS)
    if FPS == 0 or FPS is None:
        FPS = 30

    TRACK_POINTS = [
        mp_pose.PoseLandmark.RIGHT_HIP.value,
        mp_pose.PoseLandmark.RIGHT_KNEE.value,
        mp_pose.PoseLandmark.RIGHT_ANKLE.value
    ]

    prev_points = None
    movement_values = []
    frame_index = []
    frame_no = 0

    # ================= Extract Motion =================
    with st.spinner("Analyzing motion..."):
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = pose.process(rgb)

            if result.pose_landmarks:
                lm = result.pose_landmarks.landmark
                curr_points = np.array([[lm[p].x, lm[p].y] for p in TRACK_POINTS])

                if prev_points is not None:
                    diffs = np.linalg.norm(curr_points - prev_points, axis=1)
                    movement_values.append(np.mean(diffs))
                    frame_index.append(frame_no)

                prev_points = curr_points
            frame_no += 1

        cap.release()

    movement_values = np.array(movement_values)

    # ================= Rep Detection =================
    peaks, _ = find_peaks(movement_values, height=0.012, distance=16)

    GOOD_T = 0.022
    BAD_T = 0.013
    WINDOW = 12
    MAX_AMP = 0.05

    rep_feedback = []

    # ================= Rep Analysis =================
    for i, peak in enumerate(peaks):
        seg = movement_values[max(0, peak-WINDOW):min(len(movement_values), peak+WINDOW)]
        amp = float(np.max(seg) - np.min(seg))
        depth = min(100, int((amp / MAX_AMP) * 100))

        if amp >= GOOD_T:
            status, color = "GOOD", "green"
        elif amp >= BAD_T:
            status, color = "BAD", "orange"
        else:
            status, color = "POOR", "red"

        injury_risk = False
        reason = None

        if status == "POOR":
            injury_risk = True
            reason = "Very low depth may increase joint strain"

        if amp > 0.045:
            injury_risk = True
            reason = "Sudden uncontrolled movement spike"

        if i > 0 and status != "GOOD" and rep_feedback[-1]["status"] == "GOOD":
            injury_risk = True
            reason = "Quality drop after good rep (fatigue)"

        rep_feedback.append({
            "rep": i + 1,
            "frame": frame_index[peak],
            "time": round(frame_index[peak] / FPS, 2),
            "depth": depth,
            "status": status,
            "color": color,
            "injury_risk": injury_risk,
            "reason": reason
        })
# ================== KPI DASHBOARD ==================
    st.subheader("📊 Workout Summary")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Reps", len(rep_feedback))
    c2.metric("Good Reps", sum(1 for r in rep_feedback if r["status"] == "GOOD"))
    c3.metric("Needs Improvement", sum(1 for r in rep_feedback if r["status"] == "BAD"))
    c4.metric("Risky Moments", sum(1 for r in rep_feedback if r["injury_risk"]))
   
    # ================= Plot =================
    st.subheader("📈 Motion Analysis Graph")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(frame_index, movement_values, label="Avg Joint Movement", color="blue")

    ax.axhspan(GOOD_T, 0.06, color="green", alpha=0.08, label="Good Zone")
    ax.axhspan(BAD_T, GOOD_T, color="orange", alpha=0.08, label="Improve Zone")
    ax.axhspan(0, BAD_T, color="red", alpha=0.08, label="Poor Zone")

    for rep in rep_feedback:
        y = movement_values[frame_index.index(rep["frame"])]
        ax.scatter(rep["frame"], y, color=rep["color"], s=80, edgecolors="black")

    ax.set_ylim(0, 0.06)
    ax.set_xlabel("Frame")
    ax.set_ylabel("Avg Joint Movement")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

    # ================== INJURY RISK LIST ==================
    st.subheader("⚠️ Potential Injury Risk Moments")

    any_risk = False
    for r in rep_feedback:
        if r["injury_risk"]:
            any_risk = True
            st.error(
                f"Rep {r['rep']} | Time: {r['time']}s | {r['reason']}"
            )

    if not any_risk:
        st.success("No major risk patterns detected. Great form!")

    # REP TABLE ==================
    st.subheader("📋 Rep-wise Breakdown")

    df = pd.DataFrame(rep_feedback)[
        ["rep", "status", "depth", "time", "injury_risk"]
    ]
    st.dataframe(df, use_container_width=True)

    # USER FEEDBACK ==================
    if any_risk:
        st.warning(
            "Your workout shows some risky movement patterns. "
            "Review highlighted timestamps to reduce injury risk."
        )
    else:
        st.success(
            "Excellent workout! Your movements were controlled and safe."
        )
    # DOWNLOAD REPORT ==================
    csv = df.to_csv(index=False).encode("utf-8")

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.download_button(
            label="⬇️ Download Workout Report",
            data=csv,
            file_name="workout_report.csv",
            mime="text/csv"
        )