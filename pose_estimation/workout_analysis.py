import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

#MediaPipe Setup ------------------
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

#Video Input ------------------
cap = cv2.VideoCapture("input_video.mp4")

FPS = cap.get(cv2.CAP_PROP_FPS)
if FPS == 0:
    FPS = 30  # Default to 30 if unable to get FPS

# Joints to track (RIGHT SIDE)
TRACK_POINTS = [
    mp_pose.PoseLandmark.RIGHT_HIP.value,
    mp_pose.PoseLandmark.RIGHT_KNEE.value,
    mp_pose.PoseLandmark.RIGHT_ANKLE.value
]

prev_points = None
movement_values = []
frame_index = []

frame_no = 0

#Process Video ------------------
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb)

    if result.pose_landmarks:
        lm = result.pose_landmarks.landmark

        curr_points = np.array([
            [lm[p].x, lm[p].y] for p in TRACK_POINTS
        ])

        if prev_points is not None:
            # Average movement across joints
            diffs = np.linalg.norm(curr_points - prev_points, axis=1)
            avg_diff = np.mean(diffs)

            movement_values.append(avg_diff)
            frame_index.append(frame_no)

        prev_points = curr_points

    frame_no += 1

cap.release()

movement_values = np.array(movement_values)

#REP COUNT (PEAK DETECTION) ------------------
peaks, _ = find_peaks(
    movement_values,
    height=0.012,   # tuned for your video
    distance=16 
)

# ------------------ REP QUALITY ANALYSIS ------------------
GOOD_REP_THRESHOLD = 0.022
BAD_REP_THRESHOLD  = 0.013
WINDOW = 12

MAX_POSSIBLE_AMP = 0.05

rep_feedback = []
#rep quality analysis with depth score
for i, peak in enumerate(peaks):
    start = max(0, peak - WINDOW)
    end = min(len(movement_values), peak + WINDOW)

    segment = movement_values[start:end]
    amplitude = float(np.max(segment) - np.min(segment))

    depth = min(100, int((amplitude / MAX_POSSIBLE_AMP) * 100))
# Rep Quality Rules ----------------
    if amplitude >= GOOD_REP_THRESHOLD:
        status = "GOOD"
        color = "green"
        comment = "Good depth and full range of motion."
    elif amplitude >= BAD_REP_THRESHOLD:
        status = "BAD"
        color = "orange"
        comment = "Shallow movement. Try going deeper."
    else:
        status = "POOR"
        color = "red"
        comment = "Very low movement. Rep may be incorrect."

  # Injury Risk Rules ----------------
    risk_flag = False
    risk_reason = None

    # Rule 1: Poor rep → risk
    if status == "POOR":
        risk_flag = True
        risk_reason = "Very low movement depth (high strain risk)"

    # Rule 2: Sudden spike (jerky movement)
    if amplitude > 0.045:
        risk_flag = True
        risk_reason = "Sudden high spike (possible uncontrolled movement)"

    # Rule 3: Fatigue pattern (BAD after GOOD)
    if i > 0 and status != "GOOD" and rep_feedback[-1]["status"] == "GOOD":
        risk_flag = True
        risk_reason = "Quality drop after good rep (fatigue risk)"

    timestamp = round(frame_index[peak] / FPS, 2)
    # rep feedback
    rep_feedback.append({
        "rep": i + 1,
        "frame": frame_index[peak],
        "amplitude": round(amplitude, 4),
        "depth": depth,          # ✅ ONLY THIS
        "status": status,
        "color": color,
        "comment": comment,
        "injury_risk": risk_flag,
        "risk_reason": risk_reason
    })
# GRAPH ------------------
plt.figure(figsize=(10, 4))
plt.plot(frame_index, movement_values, color="blue", label="Avg Joint Movement")
#for Quality bands
plt.axhspan(GOOD_REP_THRESHOLD, 0.06, color="green", alpha=0.08, label="Good Zone")
plt.axhspan(BAD_REP_THRESHOLD, GOOD_REP_THRESHOLD, color="orange", alpha=0.08, label="Needs Improvement Zone")
plt.axhspan(0, BAD_REP_THRESHOLD, color="red", alpha=0.08, label="Poor Zone")
#
good_x, good_y = [], []
bad_x, bad_y = [], []
poor_x, poor_y = [], []

for rep in rep_feedback:
    x = rep["frame"]
    y = movement_values[frame_index.index(x)]

    if rep["status"] == "GOOD":
        good_x.append(x)
        good_y.append(y)
    elif rep["status"] == "BAD":
        bad_x.append(x)
        bad_y.append(y)
    else:  # POOR
        poor_x.append(x)
        poor_y.append(y)

# Plot reps with correct colors
plt.scatter(good_x, good_y, color="green", s=90, edgecolors="black", label="Good Reps")
plt.scatter(bad_x, bad_y, color="orange", s=90, edgecolors="black", label="Needs Improvement")
plt.scatter(poor_x, poor_y, color="red", s=90, edgecolors="black", label="Poor Reps")

plt.xlabel("Frame Number")
plt.ylabel("Average Joint Movement")
plt.title("Workout Motion Analysis with Rep Quality & Depth Score")
plt.ylim(0, 0.06)
plt.grid(True)
plt.legend()
plt.show()
# FEEDBACK ------------------
print("\n===== PER-REP FEEDBACK =====")
for rep in rep_feedback:
    time_sec = round(rep["frame"] / FPS, 2)
    print(
        f"Rep {rep['rep']} | {rep['status']} | "
        f"Depth: {rep['depth']}/100 | "
        f"Amp: {rep['amplitude']} → {rep['comment']}"
        f"Frame: {rep['frame']} | Time: {time_sec}s"
    )
print("\n===== POTENTIAL INJURY RISK MOMENTS =====")
for rep in rep_feedback:
    if rep.get("injury_risk", False):
        time_sec = round(rep["frame"] / FPS, 2)
        print(
            f"⚠️ Rep {rep['rep']} at {time_sec}s (Frame {rep['frame']}) → {rep.get('risk_reason', 'Form deviation detected')}"
        )

# Summary ------------------
good_reps = sum(1 for r in rep_feedback if r["status"] == "GOOD")
bad_reps = sum(1 for r in rep_feedback if r["status"] != "GOOD")

print("\n===== WORKOUT SUMMARY =====")
print("Total Reps:", len(rep_feedback))
print("Good Reps:", sum(1 for r in rep_feedback if r["status"] == "GOOD"))
print("Needs Improvement:", sum(1 for r in rep_feedback if r["status"] == "BAD"))
print("Poor Reps:", sum(1 for r in rep_feedback if r["status"] == "POOR"))
print("Risky Moments Detected:", sum(1 for r in rep_feedback if r["injury_risk"]))