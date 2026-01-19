from email_service import send_report_email

result = send_report_email(
    "nazwanil@gmail.com",
    "Stress Test",
    "Moderate",
    6
)

print("Email sent:", result)
