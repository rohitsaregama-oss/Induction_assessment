import streamlit as st

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Medanta Induction Assessment",
    layout="centered"
)

# -------------------------------------------------
# LOGO
# -------------------------------------------------
st.image("mhpl_logo.png", width=180)
st.markdown(
    "<h2 style='text-align:center;'>MEDANTA HOSPITAL LUCKNOW</h2>",
    unsafe_allow_html=True
)

# -------------------------------------------------
# ASSESSMENT MASTER
# -------------------------------------------------
ASSESSMENTS = {
    "fire_safety": {
        "label": "🔥 Fire Safety",
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
    },
    "ipsg": {
        "label": "🛡️ IPSG",
        "questions": [
            {
                "q": "What does IPSG stand for?",
                "options": [
                    "International Patient Safety Goals",
                    "Internal Process Safety Group",
                    "Infection Prevention Safety Group",
                    "Integrated Patient Service Guide"
                ],
                "answer": "International Patient Safety Goals"
            }
        ]
    }
}

# -------------------------------------------------
# SESSION STATE INIT
# -------------------------------------------------
if "selected_assessment" not in st.session_state:
    st.session_state.selected_assessment = None

if "q_index" not in st.session_state:
    st.session_state.q_index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

# -------------------------------------------------
# PORTAL SCREEN (DROPDOWN)
# -------------------------------------------------
if st.session_state.selected_assessment is None:
    st.markdown("---")
    st.subheader("Select Assessment")

    choice = st.selectbox(
        "Assessment",
        options=[""] + list(ASSESSMENTS.keys()),
        format_func=lambda x: ASSESSMENTS[x]["label"] if x else "-- Select --"
    )

    if choice:
        st.session_state.selected_assessment = choice
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.rerun()

    st.stop()

# -------------------------------------------------
# ASSESSMENT MODE
# -------------------------------------------------
data = ASSESSMENTS[st.session_state.selected_assessment]
questions = data["questions"]

st.markdown("---")
st.subheader(data["label"])

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

    if st.button("Back to Assessment List"):
        st.session_state.selected_assessment = None
        st.rerun()

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
    key=f"q_{st.session_state.q_index}"
)

# -------------------------------------------------
# SUBMIT & NEXT
# -------------------------------------------------
if st.button("Submit & Next"):
    if answer is None:
        st.warning("Please select an option.")
        st.stop()

    if answer == q["answer"]:
        st.session_state.score += 1
        st.success("Correct ✅")
    else:
        st.error("Incorrect ❌")

    st.session_state.q_index += 1
    st.rerun()
