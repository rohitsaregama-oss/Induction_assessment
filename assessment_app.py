import streamlit as st
import requests

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="Medanta Assessment", layout="centered")

APP_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzo3YsafRiu6C9svDsDGRIykTqFbT2dOl_zkRwcSwSupNsGVikefoaYPV1plt3BGOkq/exec"

# ===============================
# READ QUERY PARAM (THIS WAS THE MISSING PART)
# ===============================
query_params = st.experimental_get_query_params()
assessment_id = query_params.get("assessment", [None])[0]

# ===============================
# HEADER
# ===============================
st.image("https://upload.wikimedia.org/wikipedia/commons/5/5f/Medanta_logo.png", width=120)
st.markdown("## MEDANTA HOSPITAL LUCKNOW")

if not assessment_id:
    st.warning("No assessment selected.")
    st.stop()

# ===============================
# SESSION STATE
# ===============================
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "questions" not in st.session_state:
    st.session_state.questions = []

# ===============================
# LOAD QUESTIONS FROM GOOGLE SHEET
# ===============================
if not st.session_state.questions:
    resp = requests.get(APP_SCRIPT_URL, params={"assessment": assessment_id})
    data = resp.json()

    if not data or "questions" not in data:
        st.error("No questions found for this assessment.")
        st.stop()

    st.session_state.questions = data["questions"]

questions = st.session_state.questions
q_index = st.session_state.q_index
total_q = len(questions)

# ===============================
# COMPLETION
# ===============================
if q_index >= total_q:
    st.success("Assessment completed")
    st.info(f"Score: {st.session_state.score}")
    st.button("Back to Assessment List", on_click=lambda: st.experimental_set_query_params())
    st.stop()

# ===============================
# SHOW QUESTION
# ===============================
q = questions[q_index]

st.markdown(f"### Question {q_index + 1} of {total_q}")
st.markdown(q["question"])

choice = st.radio(
    "Select answer",
    ["A", "B", "C", "D"],
    format_func=lambda x: q[f"option_{x.lower()}"]
)

# ===============================
# NEXT BUTTON
# ===============================
if st.button("Next"):
    if choice == q["correct"]:
        st.session_state.score += 1
    st.session_state.q_index += 1
    st.experimental_rerun()
