import streamlit as st
import time

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
GLOBAL_TIME = 60        # total test time (seconds)
QUESTION_TIME = 30      # per question time

st.set_page_config(page_title="Medanta Assessment", layout="centered")

# -------------------------------------------------
# READ URL PARAM
# -------------------------------------------------
params = st.query_params
assessment = params.get("assessment", None)

ASSESSMENTS = {
    "fire_safety": {
        "title": "🔥 Fire Safety Assessment",
        "questions": [
            {
                "q": "What is the first step in case of fire?",
                "options": [
                    "Run immediately",
                    "Raise alarm and inform security",
                    "Ignore small fires",
                    "Use water on electrical fire"
                ],
                "answer": "Raise alarm and inform security"
            }
        ]
    }
}

# -------------------------------------------------
# UI
# -------------------------------------------------
st.title("Medanta Assessment")

if not assessment:
    st.warning("No assessment selected")
    st.stop()

if assessment not in ASSESSMENTS:
    st.error("Invalid assessment link")
    st.stop()

data = ASSESSMENTS[assessment]
st.subheader(data["title"])

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
    st.session_state.q_start = time.time()
    st.session_state.q_index = 0
    st.session_state.score = 0

# -------------------------------------------------
# GLOBAL TIMER
# -------------------------------------------------
elapsed = int(time.time() - st.session_state.start_time)
remaining = GLOBAL_TIME - elapsed

if remaining <= 0:
    st.error("⏰ Time up! Assessment auto-submitted.")
    st.success(f"Final Score: {st.session_state.score}")
    st.stop()

st.info(f"⏱️ Global Time Left: {remaining} sec")

# -------------------------------------------------
# QUESTION TIMER
# -------------------------------------------------
q_elapsed = int(time.time() - st.session_state.q_start)
q_remaining = QUESTION_TIME - q_elapsed

if q_remaining <= 0:
    st.warning("⏭️ Question timed out")
    st.session_state.q_index += 1
    st.session_state.q_start = time.time()
    st.experimental_rerun()

st.warning(f"⏳ Question Time Left: {q_remaining} sec")

# -------------------------------------------------
# QUESTIONS
# -------------------------------------------------
questions = data["questions"]

if st.session_state.q_index >= len(questions):
    st.success("Assessment completed")
    st.success(f"Final Score: {st.session_state.score}")
    st.stop()

q = questions[st.session_state.q_index]

answer = st.radio(q["q"], q["options"], key=f"q{st.session_state.q_index}")

if st.button("Submit Answer"):
    if answer == q["answer"]:
        st.session_state.score += 1
        st.success("Correct ✅")
    else:
        st.error("Incorrect ❌")

    st.session_state.q_index += 1
    st.session_state.q_start = time.time()
    st.experimental_rerun()
