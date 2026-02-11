import streamlit as st
import requests

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="Medanta Assessment", layout="centered")

APP_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxl6f2x62l_1D54ZdMPT9ZML3wMDEMIxzPi9tH8aK9v1FSbiiXJNmzFB4nIDrUjO37O/exec"

# ===============================
# HEADER
# ===============================
col1, col2 = st.columns([1, 3])

with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/5f/Medanta_logo.png", width=100)

with col2:
    st.markdown("## MEDANTA HOSPITAL LUCKNOW")

st.markdown("---")

# ===============================
# READ QUERY PARAM
# ===============================
params = st.query_params
assessment_id = params.get("assessment")

# ===============================
# HOME SCREEN (NO PARAM)
# ===============================
if not assessment_id:

    st.subheader("Select Assessment")

    assessments = {
        "HR Admin Process (A01)": "A01",
        "Second Victim (A02)": "A02"
    }

    selected = st.selectbox("Choose Assessment", list(assessments.keys()))

    if st.button("Start Assessment"):
        st.query_params["assessment"] = assessments[selected]
        st.rerun()

    st.stop()

# ===============================
# SESSION STATE INIT
# ===============================
if "current_assessment" not in st.session_state:
    st.session_state.current_assessment = None

if "q_index" not in st.session_state:
    st.session_state.q_index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "questions" not in st.session_state:
    st.session_state.questions = []

# ===============================
# RESET IF ASSESSMENT CHANGES
# ===============================
if st.session_state.current_assessment != assessment_id:
    st.session_state.current_assessment = assessment_id
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.questions = []

# ===============================
# LOAD QUESTIONS
# ===============================
if not st.session_state.questions:

    try:
        resp = requests.get(
            APP_SCRIPT_URL,
            params={"assessment": assessment_id},
            timeout=10
        )

        if resp.status_code != 200:
            st.error("Failed to connect to assessment server.")
            st.stop()

        data = resp.json()

    except Exception:
        st.error("Server error. Please try again later.")
        st.stop()

    if not data or "questions" not in data or not data["questions"]:
        st.error("No questions found for this assessment.")
        st.stop()

    st.session_state.questions = data["questions"]

questions = st.session_state.questions
q_index = st.session_state.q_index
total_q = len(questions)

# ===============================
# COMPLETION SCREEN
# ===============================
if q_index >= total_q:

    st.success("Assessment Completed")
    st.info(f"Final Score: {st.session_state.score} / {total_q}")

    if st.button("Back to Home"):
        st.query_params.clear()
        st.session_state.clear()
        st.rerun()

    st.stop()

# ===============================
# QUESTION SCREEN
# ===============================
q = questions[q_index]

st.markdown(f"### Question {q_index + 1} of {total_q}")
st.markdown(q["question"])

choice = st.radio(
    "Select your answer",
    ["A", "B", "C", "D"],
    format_func=lambda x: q[f"option_{x.lower()}"]
)

if st.button("Next"):

    if choice.upper() == q["correct"].upper():
        st.session_state.score += 1

    st.session_state.q_index += 1
    st.rerun()
