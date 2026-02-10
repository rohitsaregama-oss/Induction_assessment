import streamlit as st
import requests

# ================= CONFIG =================
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzo3YsafRiu6C9svDsDGRIykTqFbT2dOl_zkRwcSwSupNsGVikefoaYPV1plt3BGOkq/exec"
LOGO_FILE = "mhpl_logo.png"

st.set_page_config(page_title="Medanta Assessment", layout="centered")

# ================= HEADER =================
try:
    st.image(LOGO_FILE, width=120)
except:
    pass

st.markdown("## **MEDANTA HOSPITAL LUCKNOW**")

# ================= READ URL PARAM =================
params = st.query_params
assessment_id = params.get("assessment", None)

if not assessment_id:
    st.warning("No assessment selected.")
    st.stop()

# ================= LOAD QUESTIONS =================
@st.cache_data(show_spinner=False)
def load_questions(aid):
    r = requests.get(APPS_SCRIPT_URL, params={"assessment": aid})
    r.raise_for_status()
    return r.json()

try:
    questions = load_questions(assessment_id)
except Exception as e:
    st.error("Unable to load assessment questions.")
    st.stop()

if not questions:
    st.warning("No active questions found for this assessment.")
    st.stop()

# ================= SESSION STATE =================
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.answers = {}

q = questions[st.session_state.q_index]

# ================= QUESTION UI =================
st.markdown(f"### 📝 {q['Assessment_Name']}")
st.markdown(f"**Question {st.session_state.q_index + 1} of {len(questions)}**")
st.markdown(q["Question_Text"])

options = {
    "A": q["Option_A"],
    "B": q["Option_B"],
    "C": q["Option_C"],
    "D": q["Option_D"]
}

choice = st.radio(
    "Select your answer",
    options.keys(),
    format_func=lambda x: f"{x}. {options[x]}",
    key=f"q_{st.session_state.q_index}"
)

# ================= NAVIGATION =================
col1, col2 = st.columns(2)

with col2:
    if st.button("Next"):
        st.session_state.answers[q["Question_ID"]] = choice
        if choice == q["Correct_Option"]:
            st.session_state.score += 1

        if st.session_state.q_index + 1 < len(questions):
            st.session_state.q_index += 1
            st.rerun()
        else:
            st.session_state.q_index = "done"
            st.rerun()

# ================= RESULT =================
if st.session_state.q_index == "done":
    st.success("Assessment completed")
    st.info(f"Score: {st.session_state.score} / {len(questions)}")
    st.stop()
