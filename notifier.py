import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Dict

try:
    from .config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_FROM, EMAIL_TO, SMTP_USE_SSL
except ImportError:
    import os
    import sys

    package_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if package_root not in sys.path:
        sys.path.insert(0, package_root)

    from job_finder_pt.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_FROM, EMAIL_TO, SMTP_USE_SSL


def send_email(new_items: List[Dict]):
    if not new_items:
        return False
    if not SMTP_HOST or not SMTP_USER or not SMTP_PASS:
        raise RuntimeError("SMTP not configured in environment variables")

    recipients = [address.strip() for address in str(EMAIL_TO).split(",") if address.strip()]
    if not recipients:
        raise RuntimeError("No recipient configured in JOBFINDER_TO")

    subject = f"Novas vagas encontradas: {len(new_items)}"
    body_lines = []
    for it in new_items:
        body_lines.append(f"{it.get('title')}\n{it.get('url')}\nSource: {it.get('source')}\n---\n")
    body = "\n".join(body_lines)

    msg = MIMEMultipart()
    msg["From"] = SMTP_FROM or SMTP_USER
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    use_ssl = SMTP_USE_SSL or SMTP_PORT == 465
    smtp_class = smtplib.SMTP_SSL if use_ssl else smtplib.SMTP

    with smtp_class(SMTP_HOST, SMTP_PORT) as server:
        if not use_ssl:
            server.ehlo()
            server.starttls()
            server.ehlo()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(msg["From"], recipients, msg.as_string())
    return True
