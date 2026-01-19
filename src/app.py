import streamlit as st
import pandas as pd
from predict import predict_risk
from email_service import send_report_email

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Mental Health Prediction Portal",
    layout="centered"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #eef2ff, #f8fafc);
    font-family: "Segoe UI", sans-serif;
}
section.main > div {
    max-width: 950px;
    margin: auto;
}
.header {
    background: linear-gradient(135deg, #6366f1, #3b82f6);
    padding: 36px;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-bottom: 35px;
    box-shadow: 0 12px 30px rgba(59,130,246,0.35);
}
.card {
    background: white;
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(15,23,42,0.08);
    margin-bottom: 30px;
    border-left: 6px solid #6366f1;
}
.result-high {
    background: #fee2e2;
    color: #b91c1c;
    padding: 18px;
    border-radius: 14px;
    font-weight: 700;
}
.result-medium {
    background: #ffedd5;
    color: #c2410c;
    padding: 18px;
    border-radius: 14px;
    font-weight: 700;
}
.result-low {
    background: #dcfce7;
    color: #166534;
    padding: 18px;
    border-radius: 14px;
    font-weight: 700;
}
.footer {
    text-align: center;
    color: #64748b;
    font-size: 13px;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ================= CONSTANTS =================
OPTIONS = {
    "Never": 0,
    "Rarely": 1,
    "Sometimes": 2,
    "Often": 3,
    "Always": 4
}

TESTS = {
    "Anxiety Test": {
        "liwc_anxiety": "I feel anxious or worried",
        "sent_neg": "I feel nervous or uneasy",
        "sent_compound": "My thoughts feel overwhelming",
        "isolation_total": "I avoid situations due to anxiety"
    },
    "Depression Test": {
        "liwc_sadness": "I feel sad or hopeless",
        "sent_neg": "I feel emotionally low",
        "isolation_total": "I prefer to stay alone",
        "sent_pos": "I rarely feel motivated or happy"
    },
    "Stress Test": {
        "economic_stress_total": "I feel financial pressure",
        "domestic_stress_total": "I feel work or home stress",
        "sent_compound": "Stress affects my thinking",
        "sent_neg": "Stress causes negative emotions"
    },
    "Daily Well-Being Check": {
        "sent_pos": "I feel positive during the day",
        "isolation_total": "I feel socially connected",
        "domestic_stress_total": "Daily responsibilities feel manageable",
        "economic_stress_total": "Money worries affect my mood"
    },
    "Overall Mental Health (AI)": {
        "sent_neg": "I feel negative emotions",
        "sent_pos": "I feel positive emotions",
        "liwc_anxiety": "I feel anxious",
        "liwc_sadness": "I feel sad",
        "economic_stress_total": "I feel financial stress",
        "isolation_total": "I feel isolated",
        "substance_use_total": "I rely on substances",
        "suicidality_total": "I have thoughts of self-harm"
    }
}

# ================= SESSION =================
if "history" not in st.session_state:
    st.session_state.history = []

# ================= HEADER =================
st.markdown("""
<div class="header">
    <h1>🧠 Mental Health Prediction Portal</h1>
    <p>AI-based self-assessment using real social media mental health data</p>
</div>
""", unsafe_allow_html=True)

# ================= TEST SELECTION =================
test_type = st.radio("Select Assessment", list(TESTS.keys()), horizontal=True)

# ================= INPUT =================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader(test_type)

responses = {}
for feature, question in TESTS[test_type].items():
    responses[feature] = OPTIONS[
        st.radio(question, OPTIONS.keys(), horizontal=True, key=feature)
    ]

st.markdown("### 🧭 Overall Mood Today")
daily_mood = st.slider("Rate your mood today", 1, 10, 5)
st.markdown("</div>", unsafe_allow_html=True)

# ================= EXTRA INPUTS =================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("✍️ Free Text Mood Input (Optional)")
user_text = st.text_area("Describe how you feel")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📧 Email Report (Optional)")
user_email = st.text_input("Enter your email")
st.markdown("</div>", unsafe_allow_html=True)

# ================= SCORING =================
def severity_level(score):
    if score >= 12:
        return "High"
    elif score >= 6:
        return "Moderate"
    return "Low"

def calculate_progress(score, severity):
    progress = min(int((score / 20) * 100), 100)
    if severity == "High":
        progress = max(progress, 80)
    elif severity == "Moderate":
        progress = max(progress, 55)
    else:
        progress = max(progress, 30)
    return progress

# ================= RESULT =================
if st.button("🔍 Get Result"):
    score = sum(responses.values()) + (daily_mood // 2)
    severity = severity_level(score)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Assessment Results")

    if test_type != "Overall Mental Health (AI)":
        st.markdown(
            f"<div class='result-{severity.lower()}'>Severity Level: {severity}</div>",
            unsafe_allow_html=True
        )
    else:
        risk, confidence = predict_risk(responses)
        st.markdown(
            f"<div class='result-{risk}'>Overall Risk: {risk.title()}</div>",
            unsafe_allow_html=True
        )
        st.write(f"Model Confidence: {confidence*100:.1f}%")

    # ================= PROGRESS REPORT =================
    st.markdown("### 📈 Progress Report")
    progress = calculate_progress(score, severity)
    st.progress(progress)

    col1, col2, col3 = st.columns(3)
    col1.metric("Score", score)
    col2.metric("Severity", severity)
    col3.metric("Progress", f"{progress}%")

    st.markdown("""
    <div style="background:#f1f5f9;padding:16px;border-radius:12px;margin-top:15px;">
    <b>Progress Interpretation</b><br>
    • Below 40% → Needs improvement<br>
    • 40–70% → Manageable condition<br>
    • Above 70% → Critical attention advised
    </div>
    """, unsafe_allow_html=True)

    # ================= EMAIL =================
    if user_email:
        try:
            send_report_email(user_email, test_type, severity, score)
            st.success("📧 Report sent to email")
        except:
            st.warning("Email could not be sent")

    # ================= SAFETY =================
    if responses.get("suicidality_total", 0) >= 3:
        st.error("If you feel unsafe, please seek immediate professional help.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.session_state.history.append({
        "Test": test_type,
        "Score": score,
        "Severity": severity
    })

# ================= HISTORY =================
with st.expander("🕒 Assessment History"):
    if st.session_state.history:
        st.table(pd.DataFrame(st.session_state.history))
    else:
        st.info("No assessments yet")

# ================= FOOTER =================
st.markdown("<div class='footer'>Educational use only | Not a medical diagnosis</div>", unsafe_allow_html=True)
