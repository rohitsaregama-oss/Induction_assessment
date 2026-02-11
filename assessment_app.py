import streamlit as st
import requests

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="Medanta Assessment", layout="centered")

APP_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxl6f2x62l_1D54ZdMPT9ZML3wMDEMIxzPi9tH8aK9v1FSbiiXJNmzFB4nIDrUjO37O/exec"

# ===============================
# READ QUERY PARAM
# ===============================
params = st.query_params
assessment_id = params.get("assessment")

# ===============================
# HEADER
# ===============================
st.image("https://upload.wikimedia.org/wikipedia/commons/5/5f/Medanta_logo.png", width=150)
st.markdown("## MEDANTA HOSPITAL LUCKNOW")
st.markdown("---")

if not assessment_id:
    st.warning("No assessment selected.")
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
# LOAD QUESTIONS (SAFE VERSION)
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

# ===============================
# VARIABLES
# ===============================
questions = st.session_state.questions
q_index = st.session_state.q_index
total_q = len(questions)

# ===============================
# COMPLETION SCREEN
# ===============================
if q_index >= total_q:
    st.success("Assessment completed successfully.")
    st.info(f"Final Score: {st.session_state.score} / {total_q}")

    if st.button("Restart Assessment"):
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.rerun()

    st.stop()

# ===============================
# DISPLAY QUESTION
# ===============================
q = questions[q_index]

st.markdown(f"### Question {q_index + 1} of {total_q}")
st.markdown(q["question"])

choice = st.radio(
    "Select your answer",
    ["A", "B", "C", "D"],
    format_func=lambda x: q[f"option_{x.lower()}"]
)

# ===============================
# NEXT BUTTON
# ===============================
if st.button("Next"):

    if choice.upper() == q["correct"].upper():
        st.session_state.score += 1

    st.session_state.q_index += 1
    st.rerun()
