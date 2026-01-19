import smtplib
import re
from email.message import EmailMessage

# ================= CONFIG =================
SENDER_EMAIL = "nazwaniv@gmail.com"
APP_PASSWORD = "drqggtebezulmuqp"

# ================= VALIDATION =================
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# ================= MAIN FUNCTION =================
def send_report_email(to_email, test_type, severity, score):
    try:
        # ---- validate email ----
        if not to_email or not is_valid_email(to_email):
            print("EMAIL ERROR: Invalid recipient email")
            return False

        msg = EmailMessage()
        msg["Subject"] = "Mental Health Assessment Report"
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email

        msg.set_content(f"""
Hello,

Your Mental Health Assessment is complete.

Assessment Type : {test_type}
Severity Level  : {severity}
Score           : {score}

⚠️ This report is for educational purposes only.
It is not a medical diagnosis.

If you are feeling unsafe or distressed,
please seek professional help immediately.

Regards,
Mental Health Prediction Portal
        """)

        # ---- Gmail SMTP (SSL) ----
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)

        return True

    except Exception as e:
        print("EMAIL ERROR:", e)
        return False
