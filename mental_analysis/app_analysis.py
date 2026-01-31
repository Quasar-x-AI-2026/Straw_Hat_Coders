import streamlit as st

from screeners.phq9 import PHQ9
from screeners.gad7 import GAD7
from screeners.who5 import WHO5

from ui.screener_ui import render_screener
#from ui.dashboard import render_dashboard

from logic.scoring import score_phq9, score_gad7, score_who5, score_dass21
from logic.storage import save_result

from screeners.dass21 import DASS21
from ui.screener_ui import render_dass21
from logic.scoring import score_dass21
from mental_analysis.ui.dashboard import render_dashboard

st.set_page_config(layout="wide")
st.title("Mental Health Companion")
st.caption("Self-reflection & screening tool — not medical advice")

mode = st.sidebar.radio(
    "Mode",
    ["Assessments", "Dashboard"]
)

if mode == "Assessments":
    tool = st.selectbox(
        "Choose an assessment",
        ["PHQ-9", "GAD-7", "WHO-5", "DASS-21"]
    )

    if tool == "PHQ-9":
        responses = render_screener(PHQ9)
        if st.button("Submit PHQ-9"):
            score, severity = score_phq9(responses)
            save_result("PHQ-9", score, severity)
            st.success(f"Score: {score} ({severity})")

    elif tool == "GAD-7":
        responses = render_screener(GAD7)
        if st.button("Submit GAD-7"):
            score, severity = score_gad7(responses)
            save_result("GAD-7", score, severity)
            st.success(f"Score: {score} ({severity})")

    elif tool == "WHO-5":
        responses = render_screener(WHO5)
        if st.button("Submit WHO-5"):
            raw, pct = score_who5(responses)
            save_result("WHO-5", pct, extra=raw)
            st.success(f"Well-being: {pct}%")
    
    elif tool == "DASS-21":
        st.warning(
            "DASS-21 assesses Depression, Anxiety, and Stress. "
            "Answer based on how you felt over the past week."
        )
        responses = render_dass21(DASS21)
        
        if st.button("Submit DASS-21"):
            scores = score_dass21(responses, DASS21["questions"])
            for subscale, score in scores.items():
                save_result(
                    tool="DASS-21",
                    subscale=subscale,
                    score=score
                    )

            st.success("DASS-21 results saved.")

            col1, col2, col3 = st.columns(3)
            col1.metric("Depression", scores["Depression"])
            col2.metric("Anxiety", scores["Anxiety"])
            col3.metric("Stress", scores["Stress"])


elif mode == "Dashboard":
    render_dashboard()

