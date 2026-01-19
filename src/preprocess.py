import streamlit as st
import pandas as pd
from predict import predict_risk

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Mental Health Prediction Portal",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #f6f9fc;
}
.main-title {
    font-size: 38px;
    font-weight: 700;
    text-align: center;
    color: #2c3e50;
}
.subtitle {
    text-align: center;
    color: #555;
    margin-bottom: 30px;
}
.card {
    background: #ffffff;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}
.result-high {
    color: #c0392b;
    font-weight: 600;
}
.result-medium {
    color: #f39c12;
    font-weight: 600;
}
.result-low {
    color: #27ae60;
    font-weight: 600;
}
.footer {
    text-align: center;
    color: #777;
    margin-top: 40px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- CONSTANTS ----------------
OPTIONS = {
    "Never": 0,
    "Rarely": 1,
    "Sometimes": 2,
    "Often": 3,
    "Always": 4
}

# Tests mapped to dataset features
TESTS = {
    "Anxiety Test": {
        "liwc_anxiety": "I feel anxious or worried",
        "sent_neg": "I feel nervous or uneasy",
        "sent_compound": "My thoughts race or feel intense"
    },
    "Depression Test": {
        "liwc_sadness": "I feel sad or hopeless",
        "liwc_negative_emotion": "I feel emotionally low",
        "sent_neg": "I feel negative emotions frequently"
    },
    "Stress Test": {
        "economic_stress_total": "I am stressed about finances",
        "domestic_stress_total": "I feel stress at home or work",
        "isolation_total": "I feel overwhelmed or isolated"
    },
    "Overall Mental Health (AI)": {
        "sent_neg": "I feel negative emotions",
        "sent_pos": "I feel positive emotions",
        "sent_compound": "My emotions feel intense",
        "liwc_anxiety": "I feel anxious",
        "liwc_sadness": "I feel sad",
        "liwc_negative_emotion": "I use negative emotional language",
        "liwc_positive_emotion": "I use positive emotional language",
        "economic_stress_total": "I am stressed financially",
        "isolation_total": "I feel isolated",
        "domestic_stress_total": "I feel stress at home",
        "substance_use_total": "I rely on alcohol or substances",
        "suicidality_total": "I have thoughts of self-harm"
    }
}

# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- HEADER ----------------
st.markdown("<div class='main-title'>🧠 Mental Health Prediction Portal</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-powered self-assessment using social media mental health data</div>", unsafe_allow_html=True)

# ---------------- TEST SELECTION ----------------
test_type = st.radio(
    "Select a Mental Health Test",
    list(TESTS.keys()),
    horizontal=True
)

# ---------------- TEST CARD ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader(test_type)

responses = {}

for feature, question in TESTS[test_type].items():
    choice = st.radio(
        question,
        list(OPTIONS.keys()),
        horizontal=True,
        key=feature
    )
    responses[feature] = OPTIONS[choice]

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- PREDICT BUTTON ----------------
if st.button("🔍 Get Result"):
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    # Simple score for non-AI tests
    score = sum(responses.values())

    if test_type != "Overall Mental Health (AI)":
        if score >= 8:
            st.markdown("<p class='result-high'>High Level Detected</p>", unsafe_allow_html=True)
            st.write("Recommendation: Consider stress-management techniques or professional support.")
        elif score >= 4:
            st.markdown("<p class='result-medium'>Moderate Level Detected</p>", unsafe_allow_html=True)
            st.write("Recommendation: Monitor symptoms and practice self-care.")
        else:
            st.markdown("<p class='result-low'>Low Level Detected</p>", unsafe_allow_html=True)
            st.write("Recommendation: Maintain healthy habits.")
    else:
        risk, confidence = predict_risk(responses)

        if risk == "high":
            st.markdown("<p class='result-high'>High Mental Health Risk</p>", unsafe_allow_html=True)
        elif risk == "medium":
            st.markdown("<p class='result-medium'>Medium Mental Health Risk</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p class='result-low'>Low Mental Health Risk</p>", unsafe_allow_html=True)

        st.write(f"Model Confidence: {confidence}")

    st.markdown("</div>", unsafe_allow_html=True)

    st.session_state.history.append({
        "Test": test_type,
        "Result": score if test_type != "Overall Mental Health (AI)" else risk
    })

# ---------------- HISTORY ----------------
with st.expander("🕒 View Test History"):
    if not st.session_state.history:
        st.info("No tests taken yet.")
    else:
        st.table(pd.DataFrame(st.session_state.history))

# ---------------- FOOTER ----------------
st.markdown("<div class='footer'>Educational use only | Not a medical diagnosis</div>", unsafe_allow_html=True)
