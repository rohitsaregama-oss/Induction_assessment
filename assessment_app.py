import streamlit as st

st.set_page_config(page_title="Medanta Induction Assessment", layout="centered")

# ---------------- LOGO ----------------
st.image("mhpl_logo.png", width=180)
st.markdown("<h2 style='text-align:center;'>MEDANTA HOSPITAL LUCKNOW</h2>", unsafe_allow_html=True)

# ---------------- MASTER ----------------
ASSESSMENTS = {
    "hr_admin_process": "📋 HR Admin Process",
    "second_victim": "🧠 Second Victim",
    "medication_safety": "💊 Medication Safety",
    "blood_blood_product": "🩸 Blood & Blood Product",
    "basic_life_support": "❤️ Basic Life Support",
    "fire_safety": "🔥 Fire Safety",
    "infection_prevention": "🧼 Infection Prevention",
    "quality_training": "📊 Quality Training",
    "ipsg": "🛡️ IPSG",
    "radiation_training": "☢️ Radiation Training",
    "facility_mgmt_safety": "🏥 Facility Management Safety",
    "emergency_codes": "🚨 Emergency Codes",
    "cybersecurity_assessment": "🔐 Cybersecurity",
    "workplace_violence": "⚠️ Workplace Violence",
    "emr_training": "💻 EMR Training",
    "his_training": "🖥️ HIS Training",
    "medical_documentation": "📝 Medical Documentation"
}

QUESTIONS = {
    "fire_safety": [
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

# ---------------- STATE ----------------
if "assessment" not in st.session_state:
    st.session_state.assessment = None
    st.session_state.q_index = 0
    st.session_state.score = 0

# ---------------- PORTAL ----------------
if st.session_state.assessment is None:
    st.subheader("Select Assessment")

    choice = st.radio(
        label="",
        options=list(ASSESSMENTS.keys()),
        format_func=lambda x: ASSESSMENTS[x]
    )

    if st.button("Start Assessment"):
        st.session_state.assessment = choice
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.rerun()

    st.stop()

# ---------------- ASSESSMENT ----------------
assessment = st.session_state.assessment
st.subheader(ASSESSMENTS[assessment])

qs = QUESTIONS.get(assessment, [])

if st.session_state.q_index >= len(qs):
    st.success("Assessment completed")
    st.info(f"Score: {st.session_state.score}")
    if st.button("Back to Assessment List"):
        st.session_state.assessment = None
        st.rerun()
    st.stop()

q = qs[st.session_state.q_index]

answer = st.radio(
    q["q"],
    q["options"],
    key=f"q_{st.session_state.q_index}"
)

if st.button("Submit & Next"):
    if answer == q["answer"]:
        st.session_state.score += 1
    st.session_state.q_index += 1
    st.rerun()
