import streamlit as st

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Medanta Induction Assessment",
    layout="centered"
)

# -------------------------------------------------
# SAFE LOGO LOAD (won’t silently fail)
# -------------------------------------------------
try:
    st.image("mhpl_logo.png", width=180)
except Exception:
    st.error("⚠️ Logo file not found. Ensure mhpl_logo.png is in repo root.")

st.markdown(
    "<h2 style='text-align:center;'>MEDANTA HOSPITAL LUCKNOW</h2>",
    unsafe_allow_html=True
)

# -------------------------------------------------
# URL PARAM
# -------------------------------------------------
params = st.query_params
assessment = params.get("assessment")

# -------------------------------------------------
# ASSESSMENT DATA
# -------------------------------------------------
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
            },
            {
                "q": "Which extinguisher is used for electrical fires?",
                "options": [
                    "Water",
                    "Foam",
                    "CO₂",
                    "Sand"
                ],
                "answer": "CO₂"
            }
        ]
    }
}

# -------------------------------------------------
# VALIDATION
# -------------------------------------------------
if not assessment:
    st.warning("No assessment selected")
    st.stop()

if assessment not in ASSESSMENTS:
    st.error("Invalid assessment link")
    st.stop()

data = ASSESSMENTS[assessment]

# -------------------------------------------------
# SESSION STATE INIT (HARD RESET SAFE)
# -------------------------------------------------
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.last_answer = None

questions = data["questions"]

st.subheader(data["title"])
st.markdown("---")

# -------------------------------------------------
# COMPLETION
# -------------------------------------------------
if st.session_state.q_index >= len(questions):
    st.success("Assessment Completed ✅")
    st.info(f"Final Score: {st.session_state.score} / {len(questions)}")
    st.markdown("---")
    st.caption(
        "This is an assessment preview strictly for internal purposes. "
        "Sharing outside Medanta Hospital, Lucknow is strictly prohibited."
    )
    st.stop()

# -------------------------------------------------
# CURRENT QUESTION
# -------------------------------------------------
q = questions[st.session_state.q_index]

st.write(f"**Question {st.session_state.q_index + 1} of {len(questions)}**")

answer = st.radio(
    q["q"],
    q["options"],
    index=None,
    key=f"question_{st.session_state.q_index}"
)

# -------------------------------------------------
# SUBMIT LOGIC (GUARANTEED ADVANCE)
# -------------------------------------------------
if st.button("Submit & Next", key=f"submit_{st.session_state.q_index}"):
    if answer is None:
        st.warning("Please select an option before continuing.")
        st.stop()

    if answer == q["answer"]:
        st.session_state.score += 1
        st.success("Correct ✅")
    else:
        st.error("Incorrect ❌")

    # advance
    st.session_state.q_index += 1

    # force clean rerun
    st.rerun()
