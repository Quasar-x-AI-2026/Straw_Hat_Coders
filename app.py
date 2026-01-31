import streamlit as st
import subprocess
import sys
from pathlib import Path

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Health App Launcher",
    layout="wide",
)

# ---------- HIDE STREAMLIT UI ----------
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- CUSTOM CSS ----------
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    }

    .hero {
        text-align: center;
        padding: 80px 20px 40px;
        color: white;
    }

    .hero h1 {
        font-size: 3.2rem;
        font-weight: 700;
    }

    .hero p {
        font-size: 1.2rem;
        opacity: 0.85;
        margin-top: 10px;
    }

    .card {
        background: rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
    }

    .card h2 {
        margin-bottom: 10px;
    }

    .card p {
        opacity: 0.85;
    }

    .stButton > button {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white;
        border: none;
        padding: 12px 20px;
        font-size: 1rem;
        border-radius: 12px;
        margin-top: 20px;
        width: 100%;
    }

    .stButton > button:hover {
        opacity: 0.9;
        transform: scale(1.02);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- HERO SECTION ----------
st.markdown(
    """
    <div class="hero">
        <h1>Health Intelligence Platform</h1>
        <p>AI-powered mental health analysis & conversational support</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- APP LOGIC ----------
BASE_DIR = Path(__file__).resolve().parent

col1, col2 = st.columns(2, gap="large")

with col1:
    # --- Mental Health Section ---
    st.markdown(
        """
        <div class="card">
            <h2>🧠 Mental Health Analysis</h2>
            <p>Analyze emotional patterns and mental wellbeing using data-driven AI models.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Launch Analysis App", key="mental_dashboard_btn"):
        subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", str(BASE_DIR / "mental_analysis" / "app_analysis.py")]
        )
        st.success("Mental Analysis app launched")

    st.write("---") # Visual separator

    # --- Pose Estimation Section ---
    st.markdown(
        """
        <div class="card">
            <h3>🧍 Pose Estimation</h3>
            <p>Analyze posture and movement patterns as part of health intelligence.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Launch Pose Estimate", key="pose_estimation_btn"):
        subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", str(BASE_DIR / "pose_estimation" / "app.py")]
        )
        st.success("Pose Estimation app launched")

with col2:
    # --- Chatbot Section ---
    st.markdown(
        """
        <div class="card">
            <h2>💬 Health Chatbot</h2>
            <p>Chat with an AI assistant designed to support mental wellness and guidance.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Launch Chatbot", key="launch_chatbot_btn"):
        subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", str(BASE_DIR / "chatbot" / "chatbot.py")]
        )
        st.success("Chatbot app launched")

    st.write("---") # Visual separator

    # --- NEW: Clinical Feature Section ---
    st.markdown(
        """
        <div class="card">
            <h2>🏥 Clinical Features</h2>
            <p>Access specialized clinical tools, patient metrics, and diagnostic reporting.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Launch Clinical Feature", key="clinical_feature_btn"):
        subprocess.Popen(
            [
                sys.executable, 
                "-m", 
                "streamlit", 
                "run", 
                str(BASE_DIR / "clinical_report" / "main.py") # Ensure this path is correct
            ]
        )
        st.success("Clinical Feature app launched")