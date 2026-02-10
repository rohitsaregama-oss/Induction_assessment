import streamlit as st

query = st.query_params
assessment = query.get("assessment", [""])[0]

st.title("Medanta Assessment")

if assessment == "":
    st.warning("No assessment selected")
elif assessment == "fire_safety":
    st.header("Fire Safety Assessment")
elif assessment == "ipsg":
    st.header("IPSG Assessment")
elif assessment == "bls":
    st.header("Basic Life Support Assessment")
