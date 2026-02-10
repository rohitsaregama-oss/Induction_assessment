import streamlit as st
import time

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Medanta Induction", layout="centered")

ASSESSMENTS = {
    "fire_safety": "🔥 Fire Safety",
    "ipsg": "🛡️ IPSG",
    "bls": "❤️ Basic Life Support",
    "hr_admin": "📋 HR Admin Process",
    "second_victim": "🧠 Second Victim",
    "medication_safety": "💊 Medication Safety",
    "infection_prevention": "🧼 Infection Prevention",
    "blood_product": "🩸 Blood & Blood Product",
    "quality_training": "📊 Quality Training",
    "radiation_training": "☢️ Radiation Safety",
    "facility_safety": "🏥 Facility Safety",
    "emergency_codes": "🚨 Emergency Codes",
    "cybersecurity": "🔐 Cybersecurity",
    "workplace_violence": "⚠️ Workplace Violence",
    "emr": "💻 EMR Training",
    "his": "🖥️ HIS Training",
    "medical_documentation": "📝 Medical Documentation"
}

# ---------------- READ URL ----------------
params = st.query_params
current_assessment = params.get("assessment", None)

# ---------------- PORTAL MODE ----------------
if not current_assessment:
    st.title("MEDANTA HOSPITAL LUCKNOW")
    st.subheader("Induction Assessment Portal")

    choice = st.selectbox(
        "Select Assessment",
        options=[""] + list(ASSESSMENTS.keys()),
        format_func=lambda x: ASSESSMENTS.get(x, "") if x else "-- Select --"
    )

    if choice:
        base_url = st.get_option("browser.serverAddress")
        port = st.get_option("browser.serverPort")

        # Build SAME-APP link
        link = f"?assessment={choice}"

        st.success("Assessment ready")
        st.markdown(f"### 👉 [Start {ASSESSMENTS[choice]}]({link})")

    st.stop()

# ---------------- ASSESSMENT MODE ----------------
if current_assessment not in ASSESSMENTS:
    st.error("Invalid assessment link")
    st.stop()

st.title(ASSESSMENTS[current_assessment])
st.info("Assessment started")

# ---------------- SAMPLE QUESTION ----------------
QUESTION = {
    "q": "What is the first step in case of fire?",
    "options": [
        "Run immediately",
        "Raise alarm and inform security",
        "Ignore small fires",
        "Use water on electrical fire"
    ],
    "answer": "Raise alarm and inform security"
}

answer = st.radio(QUESTION["q"], QUESTION["options"])

if st.button("Submit"):
    if answer == QUESTION["answer"]:
        st.success("Correct ✅")
    else:
        st.error("Incorrect ❌")

st.markdown("---")
st.caption("This is an assessment preview strictly for internal purposes. "
           "Sharing outside Medanta Hospital, Lucknow is prohibited.")
