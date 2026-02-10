import streamlit as st

# -------------------------------------------------
# PAGE SETUP
# -------------------------------------------------
st.set_page_config(
    page_title="Medanta Assessment",
    layout="centered"
)

st.title("Medanta Assessment")

# -------------------------------------------------
# READ URL PARAMETER
# -------------------------------------------------
params = st.query_params
assessment = params.get("assessment", None)

# -------------------------------------------------
# ASSESSMENT MASTER MAP
# -------------------------------------------------
ASSESSMENTS = {
    "fire_safety": "🔥 Fire Safety Assessment",
    "ipsg": "🛡️ IPSG Assessment",
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

# -------------------------------------------------
# UI LOGIC
# -------------------------------------------------
if not assessment:
    st.warning("No assessment selected")
    st.info("Please access this page using an assessment link.")
else:
    assessment_key = assessment.lower()

    if assessment_key not in ASSESSMENTS:
        st.error("Invalid assessment link")
    else:
        st.success(ASSESSMENTS[assessment_key])

        st.markdown("---")
        st.subheader("Instructions")
        st.write("• Read each question carefully")
        st.write("• Timer will start automatically")
        st.write("• Do not refresh the page")

        st.markdown("---")
        st.subheader("Sample Question")

        q = "What is the first step in case of fire?"
        options = [
            "Run immediately",
            "Raise alarm and inform security",
            "Ignore small fires",
            "Use water on electrical fire"
        ]

        answer = st.radio(q, options)

        if st.button("Submit Answer"):
            if answer == "Raise alarm and inform security":
                st.success("Correct answer ✅")
            else:
                st.error("Incorrect ❌")
