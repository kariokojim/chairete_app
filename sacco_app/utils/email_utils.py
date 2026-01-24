from email.message import EmailMessage
import smtplib
from flask import current_app

def send_email(to_email, subject, body, attachments=None):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = current_app.config['SMTP_USER']
    msg['To'] = to_email
    msg.set_content(body)

    if attachments:
        for filename, file_bytes, mime_type in attachments:
            msg.add_attachment(
                file_bytes,
                maintype=mime_type.split('/')[0],
                subtype=mime_type.split('/')[1],
                filename=filename
            )

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(
            current_app.config['SMTP_USER'],
            current_app.config['SMTP_PASSWORD']
        )
        smtp.send_message(msg)

