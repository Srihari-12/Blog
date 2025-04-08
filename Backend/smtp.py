import smtplib

EMAIL_USER = "sriharivenkateswaran12@gmail.com"
EMAIL_PASS = "mbculznhpuwzahga"

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    print("✅ Login success")
except Exception as e:
    print("❌ Login failed:", e)
