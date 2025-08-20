import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from django.core.mail.backends.base import BaseEmailBackend

class SendGridEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        if not email_messages:
            return
        
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sent_count = 0
        
        for email_message in email_messages:
            try:
                message = Mail(
                    from_email=email_message.from_email,
                    to_emails=[e for e in email_message.to],
                    subject=email_message.subject,
                    html_content=email_message.body
                )
                response = sg.send(message)
                if response.status_code >= 200 and response.status_code < 300:
                    sent_count += 1
            except Exception as e:
                print(f"Error al enviar correo con SendGrid: {e}")
                if not self.fail_silently:
                    raise
        
        return sent_count